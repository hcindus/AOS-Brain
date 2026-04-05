using UnityEngine;
using DaVerse.Core;

namespace DaVerse.Player
{
    /// <summary>
    /// Main player controller handling movement, physics, and state.
    /// </summary>
    [RequireComponent(typeof(CharacterController))]
    [RequireComponent(typeof(PlayerInputHandler))]
    public class PlayerController : MonoBehaviour
    {
        [Header("Movement Settings")]
        [SerializeField] private float moveSpeed = 5f;
        [SerializeField] private float sprintSpeed = 8f;
        [SerializeField] private float rotationSpeed = 10f;
        [SerializeField] private float jumpHeight = 1.5f;
        
        [Header("Physics")]
        [SerializeField] private float gravity = -9.81f;
        [SerializeField] private float groundCheckDistance = 0.1f;
        [SerializeField] private LayerMask groundLayer;
        
        [Header("References")]
        [SerializeField] private Transform cameraTransform;
        [SerializeField] private Animator animator;
        
        private CharacterController _characterController;
        private PlayerInputHandler _inputHandler;
        private Vector3 _velocity;
        private bool _isGrounded;
        private bool _isSprinting;
        
        public bool IsGrounded => _isGrounded;
        public bool IsSprinting => _isSprinting;
        public float CurrentSpeed => _isSprinting ? sprintSpeed : moveSpeed;
        
        private static readonly int SpeedHash = Animator.StringToHash("Speed");
        private static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
        private static readonly int JumpHash = Animator.StringToHash("Jump");
        
        public event System.Action OnPlayerJump;
        public event System.Action<bool> OnSprintChanged;
        
        private void Awake()
        {
            _characterController = GetComponent<CharacterController>();
            _inputHandler = GetComponent<PlayerInputHandler>();
            
            if (cameraTransform == null)
                cameraTransform = Camera.main?.transform;
        }
        
        private void OnEnable()
        {
            _inputHandler.OnJump += HandleJump;
            _inputHandler.OnSprint += HandleSprint;
        }
        
        private void OnDisable()
        {
            _inputHandler.OnJump -= HandleJump;
            _inputHandler.OnSprint -= HandleSprint;
        }
        
        private void Start()
        {
            EventBus.Publish(new PlayerSpawnedEvent { Player = this });
        }
        
        private void Update()
        {
            CheckGrounded();
            HandleMovement();
            ApplyGravity();
            UpdateAnimator();
        }
        
        private void CheckGrounded()
        {
            _isGrounded = Physics.Raycast(transform.position, Vector3.down, 
                groundCheckDistance + _characterController.skinWidth, groundLayer);
        }
        
        private void HandleMovement()
        {
            Vector2 moveInput = _inputHandler.MoveInput;
            Vector3 moveDirection = CalculateMoveDirection(moveInput);
            
            float speed = _isSprinting ? sprintSpeed : moveSpeed;
            _characterController.Move(moveDirection * speed * Time.deltaTime);
            
            // Rotation
            if (moveDirection.sqrMagnitude > 0.01f)
            {
                Quaternion targetRotation = Quaternion.LookRotation(moveDirection);
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, 
                    rotationSpeed * Time.deltaTime);
            }
        }
        
        private Vector3 CalculateMoveDirection(Vector2 input)
        {
            if (cameraTransform == null) return Vector3.zero;
            
            Vector3 forward = cameraTransform.forward;
            Vector3 right = cameraTransform.right;
            
            forward.y = 0f;
            right.y = 0f;
            
            forward.Normalize();
            right.Normalize();
            
            return (forward * input.y + right * input.x).normalized;
        }
        
        private void ApplyGravity()
        {
            if (_isGrounded && _velocity.y < 0)
                _velocity.y = -0.5f;
            else
                _velocity.y += gravity * Time.deltaTime;
            
            _characterController.Move(_velocity * Time.deltaTime);
        }
        
        private void HandleJump()
        {
            if (_isGrounded)
            {
                _velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
                animator?.SetTrigger(JumpHash);
                OnPlayerJump?.Invoke();
            }
        }
        
        private void HandleSprint(bool isSprinting)
        {
            if (_isSprinting == isSprinting) return;
            _isSprinting = isSprinting;
            OnSprintChanged?.Invoke(isSprinting);
        }
        
        private void UpdateAnimator()
        {
            if (animator == null) return;
            
            float speed = _inputHandler.MoveInput.magnitude;
            if (_isSprinting) speed *= 1.5f;
            
            animator.SetFloat(SpeedHash, speed);
            animator.SetBool(IsGroundedHash, _isGrounded);
        }
        
        public void Teleport(Vector3 position, Quaternion? rotation = null)
        {
            _characterController.enabled = false;
            transform.position = position;
            if (rotation.HasValue)
                transform.rotation = rotation.Value;
            _characterController.enabled = true;
            _velocity = Vector3.zero;
        }
    }
}
