using UnityEngine;
using DaVerse.Core;

namespace DaVerse.Inventory
{
    /// <summary>
    /// Represents a pickupable item in the world.
    /// </summary>
    public class ItemPickup : MonoBehaviour
    {
        [Header("Item")]
        [SerializeField] private InventoryItem item;
        [SerializeField] private int quantity = 1;
        
        [Header("Pickup Settings")]
        [SerializeField] private bool autoPickup = false;
        [SerializeField] private float pickupRadius = 1.5f;
        [SerializeField] private bool destroyOnPickup = true;
        
        [Header("Visuals")]
        [SerializeField] private float rotationSpeed = 50f;
        [SerializeField] private float floatAmplitude = 0.2f;
        [SerializeField] private float floatSpeed = 2f;
        
        [Header("Audio")]
        [SerializeField] private AudioClip pickupSound;
        
        private Vector3 _startPosition;
        private Collider[] _colliders;
        
        private void Start()
        {
            _startPosition = transform.position;
            
            // Instantiate world model if available
            if (item?.WorldPrefab != null)
            {
                Instantiate(item.WorldPrefab, transform);
            }
        }
        
        private void Update()
        {
            // Visual effects
            transform.Rotate(Vector3.up, rotationSpeed * Time.deltaTime);
            
            float newY = _startPosition.y + Mathf.Sin(Time.time * floatSpeed) * floatAmplitude;
            transform.position = new Vector3(transform.position.x, newY, transform.position.z);
            
            // Auto-pickup check
            if (autoPickup)
            {
                CheckAutoPickup();
            }
        }
        
        private void CheckAutoPickup()
        {
            _colliders = Physics.OverlapSphere(transform.position, pickupRadius);
            
            foreach (var collider in _colliders)
            {
                if (collider.CompareTag("Player"))
                {
                    TryPickup(collider.transform);
                    break;
                }
            }
        }
        
        /// <summary>
        /// Attempt to pick up this item.
        /// </summary>
        public bool TryPickup(Transform picker)
        {
            if (item == null) return false;
            
            if (InventorySystem.Instance == null)
            {
                Debug.LogWarning("No InventorySystem found in scene!");
                return false;
            }
            
            if (InventorySystem.Instance.AddItem(item, quantity))
            {
                PlayPickupEffects();
                
                EventBus.Publish(new ItemCollectedEvent 
                { 
                    ItemId = item.ItemId, 
                    Quantity = quantity 
                });
                
                if (destroyOnPickup)
                {
                    Destroy(gameObject);
                }
                
                return true;
            }
            
            return false;
        }
        
        private void PlayPickupEffects()
        {
            if (pickupSound != null)
                AudioSource.PlayClipAtPoint(pickupSound, transform.position);
        }
        
        private void OnDrawGizmosSelected()
        {
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(transform.position, pickupRadius);
        }
        
        // For use with Interaction system
        public void OnInteract(Transform interactor)
        {
            TryPickup(interactor);
        }
    }
}
