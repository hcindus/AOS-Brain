using UnityEngine;
using UnityEngine.InputSystem;
using System;

namespace DaVerse.Player
{
    /// <summary>
    /// Handles all player input using Unity's new Input System.
    /// </summary>
    public class PlayerInputHandler : MonoBehaviour
    {
        [Header("Input Actions")]
        [SerializeField] private InputActionAsset inputActions;
        
        [Header("Action Names")]
        [SerializeField] private string moveActionName = "Move";
        [SerializeField] private string lookActionName = "Look";
        [SerializeField] private string jumpActionName = "Jump";
        [SerializeField] private string sprintActionName = "Sprint";
        [SerializeField] private string interactActionName = "Interact";
        [SerializeField] private string pauseActionName = "Pause";
        [SerializeField] private string inventoryActionName = "Inventory";
        
        private InputAction _moveAction;
        private InputAction _lookAction;
        private InputAction _jumpAction;
        private InputAction _sprintAction;
        private InputAction _interactAction;
        private InputAction _pauseAction;
        private InputAction _inventoryAction;
        
        public Vector2 MoveInput { get; private set; }
        public Vector2 LookInput { get; private set; }
        public bool IsSprinting { get; private set; }
        
        public event Action OnJump;
        public event Action<bool> OnSprint;
        public event Action OnInteract;
        public event Action OnPause;
        public event Action OnInventoryToggle;
        
        private void Awake()
        {
            if (inputActions == null)
            {
                Debug.LogError("Input Action Asset not assigned!");
                enabled = false;
                return;
            }
            
            InitializeActions();
        }
        
        private void InitializeActions()
        {
            _moveAction = inputActions.FindAction(moveActionName);
            _lookAction = inputActions.FindAction(lookActionName);
            _jumpAction = inputActions.FindAction(jumpActionName);
            _sprintAction = inputActions.FindAction(sprintActionName);
            _interactAction = inputActions.FindAction(interactActionName);
            _pauseAction = inputActions.FindAction(pauseActionName);
            _inventoryAction = inputActions.FindAction(inventoryActionName);
        }
        
        private void OnEnable()
        {
            EnableAllActions();
            SubscribeToEvents();
        }
        
        private void OnDisable()
        {
            UnsubscribeFromEvents();
            DisableAllActions();
        }
        
        private void Update()
        {
            ReadInputValues();
        }
        
        private void ReadInputValues()
        {
            MoveInput = _moveAction?.ReadValue<Vector2>() ?? Vector2.zero;
            LookInput = _lookAction?.ReadValue<Vector2>() ?? Vector2.zero;
            IsSprinting = _sprintAction?.IsPressed() ?? false;
        }
        
        private void SubscribeToEvents()
        {
            if (_jumpAction != null)
                _jumpAction.performed += HandleJump;
            if (_sprintAction != null)
            {
                _sprintAction.started += ctx => OnSprint?.Invoke(true);
                _sprintAction.canceled += ctx => OnSprint?.Invoke(false);
            }
            if (_interactAction != null)
                _interactAction.performed += HandleInteract;
            if (_pauseAction != null)
                _pauseAction.performed += HandlePause;
            if (_inventoryAction != null)
                _inventoryAction.performed += HandleInventory;
        }
        
        private void UnsubscribeFromEvents()
        {
            if (_jumpAction != null)
                _jumpAction.performed -= HandleJump;
            if (_sprintAction != null)
            {
                _sprintAction.started -= ctx => OnSprint?.Invoke(true);
                _sprintAction.canceled -= ctx => OnSprint?.Invoke(false);
            }
            if (_interactAction != null)
                _interactAction.performed -= HandleInteract;
            if (_pauseAction != null)
                _pauseAction.performed -= HandlePause;
            if (_inventoryAction != null)
                _inventoryAction.performed -= HandleInventory;
        }
        
        private void HandleJump(InputAction.CallbackContext ctx) => OnJump?.Invoke();
        private void HandleInteract(InputAction.CallbackContext ctx) => OnInteract?.Invoke();
        private void HandlePause(InputAction.CallbackContext ctx) => OnPause?.Invoke();
        private void HandleInventory(InputAction.CallbackContext ctx) => OnInventoryToggle?.Invoke();
        
        private void EnableAllActions()
        {
            _moveAction?.Enable();
            _lookAction?.Enable();
            _jumpAction?.Enable();
            _sprintAction?.Enable();
            _interactAction?.Enable();
            _pauseAction?.Enable();
            _inventoryAction?.Enable();
        }
        
        private void DisableAllActions()
        {
            _moveAction?.Disable();
            _lookAction?.Disable();
            _jumpAction?.Disable();
            _sprintAction?.Disable();
            _interactAction?.Disable();
            _pauseAction?.Disable();
            _inventoryAction?.Disable();
        }
        
        public void SetInputEnabled(bool enabled)
        {
            if (enabled)
                EnableAllActions();
            else
                DisableAllActions();
        }
    }
}
