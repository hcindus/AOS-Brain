#!/usr/bin/env python3
"""
Skill Version Manager

Semantic versioning for brain skills with automatic compatibility checking.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Version:
    """Semantic version (MAJOR.MINOR.PATCH)."""
    major: int
    minor: int
    patch: int
    
    @classmethod
    def from_string(cls, version_str: str) -> 'Version':
        """Parse version string."""
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str)
        if not match:
            raise ValueError(f"Invalid version: {version_str}")
        return cls(int(match[1]), int(match[2]), int(match[3]))
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def __lt__(self, other: 'Version') -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
    
    def __le__(self, other: 'Version') -> bool:
        return self == other or self < other
    
    def __gt__(self, other: 'Version') -> bool:
        return not self <= other
    
    def is_compatible_with(self, other: 'Version') -> bool:
        """Check if versions are backward compatible (same major)."""
        return self.major == other.major
    
    def bump_major(self) -> 'Version':
        """Breaking changes - bump major."""
        return Version(self.major + 1, 0, 0)
    
    def bump_minor(self) -> 'Version':
        """New features - bump minor."""
        return Version(self.major, self.minor + 1, 0)
    
    def bump_patch(self) -> 'Version':
        """Bug fixes - bump patch."""
        return Version(self.major, self.minor, self.patch + 1)


@dataclass
class SkillVersion:
    """Complete version record for a skill."""
    name: str
    version: Version
    previous_version: Optional[Version]
    changelog: str
    breaking_changes: bool
    deprecated: bool
    test_results: Dict
    audit_date: str
    author: str
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'version': str(self.version),
            'previous_version': str(self.previous_version) if self.previous_version else None,
            'changelog': self.changelog,
            'breaking_changes': self.breaking_changes,
            'deprecated': self.deprecated,
            'test_results': self.test_results,
            'audit_date': self.audit_date,
            'author': self.author
        }


class SkillVersionManager:
    """Manages skill versioning and compatibility."""
    
    def __init__(self, versions_file: Optional[str] = None):
        self.versions_file = versions_file or self._default_versions_file()
        self.versions: Dict[str, List[SkillVersion]] = {}
        self._load_versions()
    
    def _default_versions_file(self) -> str:
        return str(Path.home() / '.aos' / 'brain' / 'skill_versions.json')
    
    def _load_versions(self):
        """Load version history from file."""
        if Path(self.versions_file).exists():
            with open(self.versions_file) as f:
                data = json.load(f)
                for name, versions in data.items():
                    self.versions[name] = [
                        SkillVersion(
                            name=v['name'],
                            version=Version.from_string(v['version']),
                            previous_version=Version.from_string(v['previous_version']) if v['previous_version'] else None,
                            changelog=v['changelog'],
                            breaking_changes=v['breaking_changes'],
                            deprecated=v['deprecated'],
                            test_results=v['test_results'],
                            audit_date=v['audit_date'],
                            author=v['author']
                        )
                        for v in versions
                    ]
    
    def _save_versions(self):
        """Save version history to file."""
        Path(self.versions_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.versions_file, 'w') as f:
            data = {
                name: [v.to_dict() for v in versions]
                for name, versions in self.versions.items()
            }
            json.dump(data, f, indent=2)
    
    def register_version(self, skill_version: SkillVersion):
        """Register a new skill version."""
        if skill_version.name not in self.versions:
            self.versions[skill_version.name] = []
        
        self.versions[skill_version.name].append(skill_version)
        self._save_versions()
    
    def get_latest(self, skill_name: str) -> Optional[SkillVersion]:
        """Get latest version of a skill."""
        versions = self.versions.get(skill_name, [])
        return max(versions, key=lambda v: v.version) if versions else None
    
    def get_compatible_versions(self, skill_name: str, current_version: Version) -> List[SkillVersion]:
        """Get all versions compatible with current."""
        versions = self.versions.get(skill_name, [])
        return [v for v in versions if v.version.is_compatible_with(current_version)]
    
    def bump_version(self, skill_name: str, bump_type: str, changelog: str, author: str) -> SkillVersion:
        """Bump skill version."""
        latest = self.get_latest(skill_name)
        
        if latest:
            old_version = latest.version
            if bump_type == 'major':
                new_version = old_version.bump_major()
            elif bump_type == 'minor':
                new_version = old_version.bump_minor()
            else:  # patch
                new_version = old_version.bump_patch()
        else:
            old_version = None
            new_version = Version(1, 0, 0)
        
        skill_version = SkillVersion(
            name=skill_name,
            version=new_version,
            previous_version=old_version,
            changelog=changelog,
            breaking_changes=(bump_type == 'major'),
            deprecated=False,
            test_results={},
            audit_date=datetime.now().isoformat(),
            author=author
        )
        
        self.register_version(skill_version)
        return skill_version
    
    def deprecate_version(self, skill_name: str, version: str, reason: str):
        """Mark a version as deprecated."""
        versions = self.versions.get(skill_name, [])
        for v in versions:
            if str(v.version) == version:
                v.deprecated = True
                v.changelog += f"\n[DEPRECATED] {reason}"
        self._save_versions()
    
    def generate_report(self) -> Dict:
        """Generate version report for all skills."""
        report = {}
        for name, versions in self.versions.items():
            latest = max(versions, key=lambda v: v.version)
            deprecated = [v for v in versions if v.deprecated]
            
            report[name] = {
                'total_versions': len(versions),
                'latest': str(latest.version),
                'deprecated_count': len(deprecated),
                'last_audit': latest.audit_date,
                'test_status': 'pass' if all(latest.test_results.get('passed', False) for v in versions) else 'fail'
            }
        
        return report
    
    def check_compatibility_matrix(self, skill_names: List[str]) -> Dict[str, List[str]]:
        """Check compatibility between skills."""
        matrix = {}
        for name in skill_names:
            latest = self.get_latest(name)
            if latest:
                compatible = self.get_compatible_versions(name, latest.version)
                matrix[name] = [str(v.version) for v in compatible]
        return matrix


# Singleton instance
_version_manager: Optional[SkillVersionManager] = None

def get_version_manager() -> SkillVersionManager:
    """Get or create singleton version manager."""
    global _version_manager
    if _version_manager is None:
        _version_manager = SkillVersionManager()
    return _version_manager


if __name__ == '__main__':
    # Example usage
    vm = get_version_manager()
    
    # Bump thalamus to v1.1.0
    new_version = vm.bump_version(
        'thalamus',
        'minor',
        'Added priority weighting for agent inputs',
        'miles@agi-company.ai'
    )
    
    print(f"Bumped thalamus to {new_version.version}")
    print(f"Report: {vm.generate_report()}")
