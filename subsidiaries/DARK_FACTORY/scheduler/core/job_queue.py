"""
Persistent Job Queue for Dark Factory Scheduler
==============================================

Features:
- SQLite-based persistence
- Job history tracking
- Queue recovery after restart
- Priority management
- Dead letter queue for failed jobs
"""

import sqlite3
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

from ..core.scheduler import ManufacturingJob, JobStatus, JobPriority

logger = logging.getLogger("PersistentJobQueue")


@dataclass
class QueueStats:
    """Queue statistics"""
    total_jobs: int
    pending: int
    running: int
    completed: int
    failed: int
    avg_wait_time: float
    avg_process_time: float


class PersistentJobQueue:
    """
    Persistent job queue with SQLite backend.
    Survives restarts, tracks history, handles failures.
    """
    
    def __init__(self, db_path: str = "/root/.openclaw/workspace/subsidiaries/DARK_FACTORY/scheduler/data/job_queue.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_db()
        logger.info(f"PersistentJobQueue initialized: {self.db_path}")
    
    def _init_db(self):
        """Initialize SQLite database"""
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    product_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    priority TEXT NOT NULL,
                    materials_needed TEXT NOT NULL,
                    estimated_duration INTEGER NOT NULL,
                    setup_time INTEGER NOT NULL,
                    quality_requirements TEXT,
                    inspection_points TEXT,
                    deadline TEXT,
                    status TEXT NOT NULL,
                    assigned_station TEXT,
                    assigned_agent TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    actual_duration INTEGER,
                    quality_score REAL,
                    defect_count INTEGER DEFAULT 0,
                    rework_required INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    customer_id TEXT,
                    order_id TEXT,
                    job_data TEXT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS job_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    station_id TEXT,
                    agent_id TEXT,
                    notes TEXT,
                    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
                );
                
                CREATE TABLE IF NOT EXISTS dead_letter_queue (
                    dlq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    failure_reason TEXT NOT NULL,
                    retry_count INTEGER DEFAULT 0,
                    failed_at TEXT NOT NULL,
                    last_retry_at TEXT
                );
                
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
                CREATE INDEX IF NOT EXISTS idx_jobs_priority ON jobs(priority);
                CREATE INDEX IF NOT EXISTS idx_history_job_id ON job_history(job_id);
            """)
            conn.commit()
    
    @contextmanager
    def _get_conn(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def enqueue(self, job: ManufacturingJob) -> bool:
        """Add job to queue"""
        try:
            with self._get_conn() as conn:
                conn.execute("""
                    INSERT INTO jobs (
                        job_id, product_type, quantity, priority,
                        materials_needed, estimated_duration, setup_time,
                        quality_requirements, inspection_points, deadline,
                        status, assigned_station, assigned_agent,
                        start_time, end_time, actual_duration,
                        quality_score, defect_count, rework_required,
                        created_at, customer_id, order_id, job_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.job_id,
                    job.product_type,
                    job.quantity,
                    job.priority.name,
                    json.dumps(job.materials_needed),
                    job.estimated_duration,
                    job.setup_time,
                    json.dumps(job.quality_requirements) if job.quality_requirements else None,
                    json.dumps(job.inspection_points) if job.inspection_points else None,
                    job.deadline.isoformat() if job.deadline else None,
                    job.status.value,
                    job.assigned_station,
                    job.assigned_agent,
                    job.start_time.isoformat() if job.start_time else None,
                    job.end_time.isoformat() if job.end_time else None,
                    job.actual_duration,
                    job.quality_score,
                    job.defect_count,
                    1 if job.rework_required else 0,
                    job.created_at.isoformat(),
                    job.customer_id,
                    job.order_id,
                    json.dumps(job.to_dict())
                ))
                
                # Log history
                conn.execute("""
                    INSERT INTO job_history (job_id, status, timestamp, notes)
                    VALUES (?, ?, ?, ?)
                """, (job.job_id, "ENQUEUED", datetime.now().isoformat(), "Job submitted to queue"))
                
                conn.commit()
                logger.info(f"Enqueued job: {job.job_id}")
                return True
        except sqlite3.IntegrityError:
            logger.warning(f"Job {job.job_id} already exists in queue")
            return False
        except Exception as e:
            logger.error(f"Failed to enqueue job: {e}")
            return False
    
    def dequeue(self, status_filter: Optional[JobStatus] = None) -> Optional[ManufacturingJob]:
        """Get next job from queue"""
        try:
            with self._get_conn() as conn:
                if status_filter:
                    cursor = conn.execute(
                        "SELECT job_data FROM jobs WHERE status = ? ORDER BY priority, created_at LIMIT 1",
                        (status_filter.value,)
                    )
                else:
                    cursor = conn.execute(
                        "SELECT job_data FROM jobs WHERE status IN ('pending', 'queued') ORDER BY priority, created_at LIMIT 1"
                    )
                
                row = cursor.fetchone()
                if row:
                    job_data = json.loads(row[0])
                    return ManufacturingJob.from_dict(job_data)
                return None
        except Exception as e:
            logger.error(f"Failed to dequeue job: {e}")
            return None
    
    def update_job(self, job: ManufacturingJob) -> bool:
        """Update job in queue"""
        try:
            with self._get_conn() as conn:
                conn.execute("""
                    UPDATE jobs SET
                        status = ?,
                        assigned_station = ?,
                        assigned_agent = ?,
                        start_time = ?,
                        end_time = ?,
                        actual_duration = ?,
                        quality_score = ?,
                        defect_count = ?,
                        rework_required = ?,
                        job_data = ?
                    WHERE job_id = ?
                """, (
                    job.status.value,
                    job.assigned_station,
                    job.assigned_agent,
                    job.start_time.isoformat() if job.start_time else None,
                    job.end_time.isoformat() if job.end_time else None,
                    job.actual_duration,
                    job.quality_score,
                    job.defect_count,
                    1 if job.rework_required else 0,
                    json.dumps(job.to_dict()),
                    job.job_id
                ))
                
                # Log status change
                conn.execute("""
                    INSERT INTO job_history (job_id, status, timestamp, station_id, agent_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    job.job_id,
                    job.status.value,
                    datetime.now().isoformat(),
                    job.assigned_station,
                    job.assigned_agent
                ))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to update job: {e}")
            return False
    
    def get_pending_jobs(self, limit: Optional[int] = None) -> List[ManufacturingJob]:
        """Get all pending jobs"""
        try:
            with self._get_conn() as conn:
                query = "SELECT job_data FROM jobs WHERE status IN ('pending', 'queued') ORDER BY priority, created_at"
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor = conn.execute(query)
                return [ManufacturingJob.from_dict(json.loads(row[0])) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get pending jobs: {e}")
            return []
    
    def get_running_jobs(self) -> List[ManufacturingJob]:
        """Get all running jobs"""
        try:
            with self._get_conn() as conn:
                cursor = conn.execute("SELECT job_data FROM jobs WHERE status = 'running'")
                return [ManufacturingJob.from_dict(json.loads(row[0])) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get running jobs: {e}")
            return []
    
    def get_job_history(self, job_id: str) -> List[Dict]:
        """Get history for a specific job"""
        try:
            with self._get_conn() as conn:
                cursor = conn.execute(
                    "SELECT * FROM job_history WHERE job_id = ? ORDER BY timestamp",
                    (job_id,)
                )
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get job history: {e}")
            return []
    
    def move_to_dlq(self, job_id: str, reason: str, retry_count: int = 0):
        """Move failed job to dead letter queue"""
        try:
            with self._get_conn() as conn:
                conn.execute("""
                    INSERT INTO dead_letter_queue (job_id, failure_reason, retry_count, failed_at)
                    VALUES (?, ?, ?, ?)
                """, (job_id, reason, retry_count, datetime.now().isoformat()))
                conn.commit()
                logger.warning(f"Job {job_id} moved to DLQ: {reason}")
        except Exception as e:
            logger.error(f"Failed to move job to DLQ: {e}")
    
    def retry_dlq_job(self, job_id: str) -> bool:
        """Retry a job from DLQ"""
        try:
            with self._get_conn() as conn:
                # Get job
                cursor = conn.execute("SELECT job_data FROM jobs WHERE job_id = ?", (job_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                
                job_data = json.loads(row[0])
                job_data["status"] = "pending"
                
                # Update job
                conn.execute(
                    "UPDATE jobs SET status = 'pending', job_data = ? WHERE job_id = ?",
                    (json.dumps(job_data), job_id)
                )
                
                # Update DLQ
                conn.execute(
                    "UPDATE dead_letter_queue SET retry_count = retry_count + 1, last_retry_at = ? WHERE job_id = ?",
                    (datetime.now().isoformat(), job_id)
                )
                
                conn.commit()
                logger.info(f"Job {job_id} retried from DLQ")
                return True
        except Exception as e:
            logger.error(f"Failed to retry DLQ job: {e}")
            return False
    
    def get_stats(self) -> QueueStats:
        """Get queue statistics"""
        try:
            with self._get_conn() as conn:
                # Count by status
                cursor = conn.execute("""
                    SELECT status, COUNT(*) FROM jobs GROUP BY status
                """)
                counts = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Calculate wait times
                cursor = conn.execute("""
                    SELECT AVG(CAST((julianday(start_time) - julianday(created_at)) * 24 * 60 AS INTEGER))
                    FROM jobs WHERE start_time IS NOT NULL
                """)
                avg_wait = cursor.fetchone()[0] or 0
                
                # Calculate process times
                cursor = conn.execute("""
                    SELECT AVG(actual_duration) FROM jobs WHERE actual_duration IS NOT NULL
                """)
                avg_process = cursor.fetchone()[0] or 0
                
                return QueueStats(
                    total_jobs=sum(counts.values()),
                    pending=counts.get('pending', 0) + counts.get('queued', 0),
                    running=counts.get('running', 0),
                    completed=counts.get('completed', 0),
                    failed=counts.get('failed', 0),
                    avg_wait_time=avg_wait,
                    avg_process_time=avg_process
                )
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return QueueStats(0, 0, 0, 0, 0, 0, 0)
    
    def clear_completed(self, older_than_days: int = 30) -> int:
        """Clear old completed jobs"""
        try:
            with self._get_conn() as conn:
                cursor = conn.execute("""
                    DELETE FROM jobs 
                    WHERE status = 'completed' 
                    AND datetime(created_at) < datetime('now', ?)
                """, (f"-{older_than_days} days",))
                conn.commit()
                cleared = cursor.rowcount
                logger.info(f"Cleared {cleared} old completed jobs")
                return cleared
        except Exception as e:
            logger.error(f"Failed to clear completed jobs: {e}")
            return 0
    
    def backup(self, backup_path: Optional[str] = None) -> str:
        """Backup queue database"""
        if not backup_path:
            backup_path = f"{self.db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            with self._get_conn() as conn:
                backup_conn = sqlite3.connect(backup_path)
                conn.backup(backup_conn)
                backup_conn.close()
                logger.info(f"Queue backed up to: {backup_path}")
                return backup_path
        except Exception as e:
            logger.error(f"Failed to backup queue: {e}")
            return ""
    
    def export_to_json(self, filepath: str) -> bool:
        """Export all jobs to JSON"""
        try:
            with self._get_conn() as conn:
                cursor = conn.execute("SELECT job_data FROM jobs")
                jobs = [json.loads(row[0]) for row in cursor.fetchall()]
                
                with open(filepath, 'w') as f:
                    json.dump({
                        "exported_at": datetime.now().isoformat(),
                        "total_jobs": len(jobs),
                        "jobs": jobs
                    }, f, indent=2)
                
                logger.info(f"Exported {len(jobs)} jobs to {filepath}")
                return True
        except Exception as e:
            logger.error(f"Failed to export jobs: {e}")
            return False


def main():
    """Demo persistent job queue"""
    queue = PersistentJobQueue()
    
    # Create sample jobs
    from datetime import timedelta
    
    jobs = [
        ManufacturingJob(
            job_id=f"TEST-{i:03d}",
            product_type=["prototype", "assembly", "precision"][i % 3],
            quantity=10 + i * 5,
            priority=[JobPriority.HIGH, JobPriority.MEDIUM, JobPriority.LOW][i % 3],
            materials_needed={"part_a": i + 1},
            estimated_duration=30 + i * 10,
            setup_time=10,
            deadline=datetime.now() + timedelta(hours=i + 1),
        )
        for i in range(5)
    ]
    
    # Enqueue jobs
    for job in jobs:
        queue.enqueue(job)
    
    # Get stats
    stats = queue.get_stats()
    print(f"\nQueue Stats:")
    print(f"  Total: {stats.total_jobs}")
    print(f"  Pending: {stats.pending}")
    print(f"  Running: {stats.running}")
    print(f"  Avg Wait: {stats.avg_wait_time:.1f} min")
    
    # Get pending
    pending = queue.get_pending_jobs(limit=3)
    print(f"\nTop 3 pending jobs:")
    for job in pending:
        print(f"  {job.job_id}: {job.product_type} (Priority: {job.priority.name})")
    
    # Export
    queue.export_to_json("/tmp/queue_export.json")
    
    print("\n✅ PersistentJobQueue demo complete")


if __name__ == "__main__":
    main()
