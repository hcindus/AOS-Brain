using UnityEngine;
using DaVerse.Core;

namespace DaVerse.Interaction
{
    /// <summary>
    /// Base class for all interactable objects in the game.
    /// </summary>
    public abstract class Interactable : MonoBehaviour
    {
        [Header("Interaction Settings")]
        [SerializeField] private string interactionPrompt = "Press E to Interact";
        [SerializeField] private float interactionDistance = 3f;
        [SerializeField] private bool requiresLineOfSight = true;
        [SerializeField] private bool oneTimeInteraction = false;
        
        [Header("Visual Feedback")]
        [SerializeField] private bool highlightOnHover = true;
        [SerializeField] private Color highlightColor = Color.yellow;
        
        protected bool hasBeenInteracted = false;
        protected bool isHighlighted = false;
        private Renderer[] _renderers;
        private Color[] _originalColors;
        
        public string InteractionPrompt => interactionPrompt;
        public float InteractionDistance => interactionDistance;
        public bool RequiresLineOfSight => requiresLineOfSight;
        public bool CanInteract => !oneTimeInteraction || !hasBeenInteracted;
        public bool IsHighlighted => isHighlighted;
        
        protected virtual void Awake()
        {
            if (highlightOnHover)
            {
                _renderers = GetComponentsInChildren<Renderer>();
                _originalColors = new Color[_renderers.Length];
                for (int i = 0; i < _renderers.Length; i++)
                {
                    _originalColors[i] = _renderers[i].material.color;
                }
            }
        }
        
        public virtual bool CanInteractWith(Transform interactor)
        {
            if (!CanInteract) return false;
            
            float distance = Vector3.Distance(transform.position, interactor.position);
            if (distance > interactionDistance) return false;
            
            if (requiresLineOfSight)
            {
                Vector3 direction = (transform.position - interactor.position).normalized;
                if (!Physics.Raycast(interactor.position, direction, out RaycastHit hit, interactionDistance))
                    return false;
                
                if (hit.transform != transform && !hit.transform.IsChildOf(transform))
                    return false;
            }
            
            return true;
        }
        
        public virtual void OnInteract(Transform interactor)
        {
            if (!CanInteractWith(interactor)) return;
            
            hasBeenInteracted = true;
            PerformInteraction(interactor);
            
            EventBus.Publish(new InteractionEvent 
            { 
                Interactable = this, 
                Interactor = interactor 
            });
            
            if (oneTimeInteraction)
            {
                OnInteractionCompleted();
            }
        }
        
        protected abstract void PerformInteraction(Transform interactor);
        
        protected virtual void OnInteractionCompleted()
        {
            // Override for cleanup after one-time interaction
        }
        
        public virtual void OnHoverEnter()
        {
            if (isHighlighted) return;
            isHighlighted = true;
            
            if (highlightOnHover && _renderers != null)
            {
                foreach (var renderer in _renderers)
                {
                    renderer.material.color = highlightColor;
                }
            }
        }
        
        public virtual void OnHoverExit()
        {
            if (!isHighlighted) return;
            isHighlighted = false;
            
            if (highlightOnHover && _renderers != null)
            {
                for (int i = 0; i < _renderers.Length; i++)
                {
                    _renderers[i].material.color = _originalColors[i];
                }
            }
        }
        
        protected virtual void OnDrawGizmosSelected()
        {
            Gizmos.color = Color.cyan;
            Gizmos.DrawWireSphere(transform.position, interactionDistance);
        }
    }
    
    public struct InteractionEvent : IGameEvent
    {
        public Interactable Interactable;
        public Transform Interactor;
    }
}
