using UnityEngine;
using System.Collections.Generic;
using DaVerse.Player;
using DaVerse.Core;

namespace DaVerse.Interaction
{
    /// <summary>
    /// Detects and handles interaction with nearby interactable objects.
    /// </summary>
    public class InteractionDetector : MonoBehaviour
    {
        [Header("Detection Settings")]
        [SerializeField] private float detectionRadius = 3f;
        [SerializeField] private LayerMask interactableLayer;
        [SerializeField] private bool useCameraCenter = true;
        [SerializeField] private float cameraRayDistance = 5f;
        
        [Header("UI")]
        [SerializeField] private GameObject interactionPromptPrefab;
        
        private PlayerInputHandler _inputHandler;
        private Camera _mainCamera;
        private Interactable _currentInteractable;
        private List<Interactable> _nearbyInteractables = new List<Interactable>();
        
        public Interactable CurrentInteractable => _currentInteractable;
        public event System.Action<Interactable> OnInteractableChanged;
        public event System.Action<Interactable> OnInteractableDetected;
        public event System.Action OnNoInteractableDetected;
        
        private void Awake()
        {
            _inputHandler = GetComponent<PlayerInputHandler>();
            _mainCamera = Camera.main;
        }
        
        private void OnEnable()
        {
            if (_inputHandler != null)
                _inputHandler.OnInteract += HandleInteraction;
            
            EventBus.Subscribe<PlayerSpawnedEvent>(OnPlayerSpawned);
        }
        
        private void OnDisable()
        {
            if (_inputHandler != null)
                _inputHandler.OnInteract -= HandleInteraction;
            
            EventBus.Unsubscribe<PlayerSpawnedEvent>(OnPlayerSpawned);
        }
        
        private void OnPlayerSpawned(PlayerSpawnedEvent evt)
        {
            // Refresh camera reference when player spawns
            _mainCamera = Camera.main;
        }
        
        private void Update()
        {
            DetectInteractables();
        }
        
        private void DetectInteractables()
        {
            Interactable bestInteractable = null;
            float bestScore = float.MinValue;
            
            if (useCameraCenter && _mainCamera != null)
            {
                // Raycast from camera center for precision
                Ray ray = new Ray(_mainCamera.transform.position, _mainCamera.transform.forward);
                if (Physics.Raycast(ray, out RaycastHit hit, cameraRayDistance, interactableLayer))
                {
                    var interactable = hit.collider.GetComponent<Interactable>() ?? 
                        hit.collider.GetComponentInParent<Interactable>();
                    
                    if (interactable != null && interactable.CanInteractWith(transform))
                    {
                        bestInteractable = interactable;
                        bestScore = 1000f; // Prioritize camera center
                    }
                }
            }
            
            // Fallback to radius detection
            if (bestInteractable == null)
            {
                Collider[] colliders = Physics.OverlapSphere(transform.position, detectionRadius, interactableLayer);
                
                foreach (var collider in colliders)
                {
                    var interactable = collider.GetComponent<Interactable>() ?? 
                        collider.GetComponentInParent<Interactable>();
                    
                    if (interactable == null || !interactable.CanInteractWith(transform))
                        continue;
                    
                    float score = CalculateInteractionScore(interactable);
                    if (score > bestScore)
                    {
                        bestScore = score;
                        bestInteractable = interactable;
                    }
                }
            }
            
            UpdateCurrentInteractable(bestInteractable);
        }
        
        private float CalculateInteractionScore(Interactable interactable)
        {
            // Score based on distance and facing direction
            float distance = Vector3.Distance(transform.position, interactable.transform.position);
            Vector3 direction = (interactable.transform.position - transform.position).normalized;
            float facingDot = Vector3.Dot(transform.forward, direction);
            
            // Prefer closer and more directly faced objects
            return -distance + facingDot * 2f;
        }
        
        private void UpdateCurrentInteractable(Interactable newInteractable)
        {
            if (_currentInteractable == newInteractable)
                return;
            
            // Clear old highlight
            if (_currentInteractable != null)
                _currentInteractable.OnHoverExit();
            
            _currentInteractable = newInteractable;
            
            // Set new highlight
            if (_currentInteractable != null)
            {
                _currentInteractable.OnHoverEnter();
                OnInteractableDetected?.Invoke(_currentInteractable);
            }
            else
            {
                OnNoInteractableDetected?.Invoke();
            }
            
            OnInteractableChanged?.Invoke(_currentInteractable);
        }
        
        private void HandleInteraction()
        {
            if (_currentInteractable != null)
            {
                _currentInteractable.OnInteract(transform);
            }
        }
        
        private void OnDrawGizmosSelected()
        {
            Gizmos.color = Color.green;
            Gizmos.DrawWireSphere(transform.position, detectionRadius);
            
            if (useCameraCenter && Camera.main != null)
            {
                Gizmos.color = Color.blue;
                Vector3 end = Camera.main.transform.position + Camera.main.transform.forward * cameraRayDistance;
                Gizmos.DrawLine(Camera.main.transform.position, end);
            }
        }
    }
}
