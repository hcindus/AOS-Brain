using UnityEngine;

namespace DaVerse.Player
{
    /// <summary>
    /// Third-person camera controller with smooth follow, collision detection, and multiple modes.
    /// </summary>
    public class CameraController : MonoBehaviour
    {
        [Header("Target")]
        [SerializeField] private Transform target;
        [SerializeField] private Vector3 offset = new Vector3(0, 2, -4);
        
        [Header("Follow Settings")]
        [SerializeField] private float followSpeed = 5f;
        [SerializeField] private float rotationSpeed = 3f;
        [SerializeField] private bool useSmoothFollow = true;
        
        [Header("Orbit Settings")]
        [SerializeField] private bool enableOrbit = true;
        [SerializeField] private float minVerticalAngle = -30f;
        [SerializeField] private float maxVerticalAngle = 60f;
        [SerializeField] private bool invertYAxis = false;
        
        [Header("Collision")]
        [SerializeField] private bool enableCollision = true;
        [SerializeField] private float collisionRadius = 0.3f;
        [SerializeField] private float minDistance = 1f;
        [SerializeField] private LayerMask collisionLayers;
        
        [Header("Zoom")]
        [SerializeField] private float zoomSpeed = 2f;
        [SerializeField] private float minZoom = 2f;
        [SerializeField] private float maxZoom = 10f;
        
        private float _currentZoom;
        private float _horizontalAngle;
        private float _verticalAngle;
        private Vector3 _currentVelocity;
        private float _defaultDistance;
        
        public Transform Target 
        { 
            get => target; 
            set 
            { 
                target = value; 
                if (target != null) 
                    InitializeCameraPosition();
            }
        }
        
        public CameraMode CurrentMode { get; set; } = CameraMode.ThirdPerson;
        
        private void Start()
        {
            _currentZoom = offset.magnitude;
            _defaultDistance = _currentZoom;
            
            if (target != null)
                InitializeCameraPosition();
        }
        
        private void LateUpdate()
        {
            if (target == null) return;
            
            switch (CurrentMode)
            {
                case CameraMode.ThirdPerson:
                    UpdateThirdPersonCamera();
                    break;
                case CameraMode.FirstPerson:
                    UpdateFirstPersonCamera();
                    break;
                case CameraMode.Fixed:
                    UpdateFixedCamera();
                    break;
                case CameraMode.Cinematic:
                    UpdateCinematicCamera();
                    break;
            }
        }
        
        private void InitializeCameraPosition()
        {
            Vector3 desiredPosition = target.position + offset;
            transform.position = desiredPosition;
            transform.LookAt(target);
            
            _horizontalAngle = transform.eulerAngles.y;
            _verticalAngle = transform.eulerAngles.x;
        }
        
        private void UpdateThirdPersonCamera()
        {
            // Get input
            float horizontalInput = Input.GetAxis("Mouse X");
            float verticalInput = Input.GetAxis("Mouse Y");
            float zoomInput = Input.GetAxis("Mouse ScrollWheel");
            
            // Update angles
            if (enableOrbit)
            {
                _horizontalAngle += horizontalInput * rotationSpeed;
                float verticalDelta = verticalInput * rotationSpeed * (invertYAxis ? -1 : 1);
                _verticalAngle = Mathf.Clamp(_verticalAngle - verticalDelta, minVerticalAngle, maxVerticalAngle);
            }
            
            // Update zoom
            _currentZoom = Mathf.Clamp(_currentZoom - zoomInput * zoomSpeed, minZoom, maxZoom);
            
            // Calculate desired position
            Quaternion rotation = Quaternion.Euler(_verticalAngle, _horizontalAngle, 0);
            Vector3 desiredOffset = rotation * Vector3.back * _currentZoom + Vector3.up * offset.y;
            Vector3 desiredPosition = target.position + desiredOffset;
            
            // Handle collision
            if (enableCollision)
            {
                desiredPosition = HandleCollision(target.position + Vector3.up * offset.y, desiredPosition);
            }
            
            // Apply position
            if (useSmoothFollow)
            {
                transform.position = Vector3.SmoothDamp(transform.position, desiredPosition, 
                    ref _currentVelocity, 1f / followSpeed);
            }
            else
            {
                transform.position = desiredPosition;
            }
            
            transform.LookAt(target.position + Vector3.up * offset.y * 0.5f);
        }
        
        private Vector3 HandleCollision(Vector3 targetPos, Vector3 desiredPos)
        {
            Vector3 direction = desiredPos - targetPos;
            float distance = direction.magnitude;
            direction.Normalize();
            
            if (Physics.SphereCast(targetPos, collisionRadius, direction, out RaycastHit hit, 
                distance, collisionLayers))
            {
                return targetPos + direction * Mathf.Max(hit.distance - collisionRadius, minDistance);
            }
            
            return desiredPos;
        }
        
        private void UpdateFirstPersonCamera()
        {
            transform.position = target.position + Vector3.up * 1.6f;
            
            float horizontalInput = Input.GetAxis("Mouse X");
            float verticalInput = Input.GetAxis("Mouse Y");
            
            _horizontalAngle += horizontalInput * rotationSpeed;
            float verticalDelta = verticalInput * rotationSpeed * (invertYAxis ? -1 : 1);
            _verticalAngle = Mathf.Clamp(_verticalAngle - verticalDelta, -90f, 90f);
            
            transform.rotation = Quaternion.Euler(_verticalAngle, _horizontalAngle, 0);
            target.rotation = Quaternion.Euler(0, _horizontalAngle, 0);
        }
        
        private void UpdateFixedCamera()
        {
            // Fixed camera position - only update look at
            transform.LookAt(target);
        }
        
        private void UpdateCinematicCamera()
        {
            // Placeholder for cinematic camera logic
            // Can be overridden for cutscenes
        }
        
        public void SetCameraMode(CameraMode mode)
        {
            CurrentMode = mode;
            if (target != null)
                InitializeCameraPosition();
        }
        
        public void ShakeCamera(float duration, float magnitude)
        {
            StartCoroutine(CameraShakeCoroutine(duration, magnitude));
        }
        
        private System.Collections.IEnumerator CameraShakeCoroutine(float duration, float magnitude)
        {
            Vector3 originalPosition = transform.localPosition;
            float elapsed = 0f;
            
            while (elapsed < duration)
            {
                float x = Random.Range(-1f, 1f) * magnitude;
                float y = Random.Range(-1f, 1f) * magnitude;
                
                transform.localPosition = originalPosition + new Vector3(x, y, 0);
                
                elapsed += Time.deltaTime;
                yield return null;
            }
            
            transform.localPosition = originalPosition;
        }
        
        private void OnDrawGizmosSelected()
        {
            if (target == null) return;
            
            Gizmos.color = Color.cyan;
            Gizmos.DrawWireSphere(target.position + Vector3.up * offset.y, collisionRadius);
        }
    }
    
    public enum CameraMode
    {
        ThirdPerson,
        FirstPerson,
        Fixed,
        Cinematic
    }
}
