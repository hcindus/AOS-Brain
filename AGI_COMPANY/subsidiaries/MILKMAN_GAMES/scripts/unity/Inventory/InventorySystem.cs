using UnityEngine;
using System;
using System.Collections.Generic;
using DaVerse.Core;

namespace DaVerse.Inventory
{
    /// <summary>
    /// Central inventory system managing items across the game.
    /// </summary>
    public class InventorySystem : MonoBehaviour
    {
        public static InventorySystem Instance { get; private set; }
        
        [Header("Inventory Settings")]
        [SerializeField] private int maxSlotCount = 20;
        [SerializeField] private bool unlimitedInventory = false;
        
        private Dictionary<string, InventorySlot> _items = new Dictionary<string, InventorySlot>();
        private List<string> _orderedItems = new List<string>();
        
        public int CurrentSlotCount => _items.Count;
        public int MaxSlotCount => maxSlotCount;
        public bool IsFull => !unlimitedInventory && _items.Count >= maxSlotCount;
        
        public event Action<InventoryItem, int> OnItemAdded;
        public event Action<InventoryItem, int> OnItemRemoved;
        public event Action<InventoryItem, int, int> OnItemQuantityChanged;
        public event Action OnInventoryChanged;
        
        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        
        /// <summary>
        /// Add an item to the inventory.
        /// </summary>
        public bool AddItem(InventoryItem item, int quantity = 1)
        {
            if (item == null || quantity <= 0) return false;
            
            string itemId = item.ItemId;
            
            // Check if item already exists
            if (_items.TryGetValue(itemId, out InventorySlot slot))
            {
                // Stackable items
                if (item.IsStackable)
                {
                    int oldQuantity = slot.Quantity;
                    slot.AddQuantity(quantity);
                    OnItemQuantityChanged?.Invoke(item, oldQuantity, slot.Quantity);
                }
                else
                {
                    // Non-stackable, check if we have space
                    if (!unlimitedInventory && _items.Count >= maxSlotCount)
                        return false;
                    
                    // Add as separate slot
                    string uniqueId = $"{itemId}_{Guid.NewGuid()}";
                    _items[uniqueId] = new InventorySlot(item, quantity);
                    _orderedItems.Add(uniqueId);
                    OnItemAdded?.Invoke(item, quantity);
                }
            }
            else
            {
                // New item
                if (!unlimitedInventory && _items.Count >= maxSlotCount)
                    return false;
                
                _items[itemId] = new InventorySlot(item, quantity);
                _orderedItems.Add(itemId);
                OnItemAdded?.Invoke(item, quantity);
                
                EventBus.Publish(new ItemCollectedEvent 
                { 
                    ItemId = itemId, 
                    Quantity = quantity 
                });
            }
            
            OnInventoryChanged?.Invoke();
            return true;
        }
        
        /// <summary>
        /// Remove an item from the inventory.
        /// </summary>
        public bool RemoveItem(string itemId, int quantity = 1)
        {
            if (!_items.TryGetValue(itemId, out InventorySlot slot))
                return false;
            
            if (slot.Quantity < quantity)
                return false;
            
            int oldQuantity = slot.Quantity;
            slot.RemoveQuantity(quantity);
            
            if (slot.Quantity <= 0)
            {
                _items.Remove(itemId);
                _orderedItems.Remove(itemId);
                OnItemRemoved?.Invoke(slot.Item, quantity);
            }
            else
            {
                OnItemQuantityChanged?.Invoke(slot.Item, oldQuantity, slot.Quantity);
            }
            
            OnInventoryChanged?.Invoke();
            return true;
        }
        
        /// <summary>
        /// Check if inventory contains an item.
        /// </summary>
        public bool HasItem(string itemId, int quantity = 1)
        {
            if (_items.TryGetValue(itemId, out InventorySlot slot))
                return slot.Quantity >= quantity;
            return false;
        }
        
        /// <summary>
        /// Get the quantity of a specific item.
        /// </summary>
        public int GetItemQuantity(string itemId)
        {
            if (_items.TryGetValue(itemId, out InventorySlot slot))
                return slot.Quantity;
            return 0;
        }
        
        /// <summary>
        /// Get all inventory items.
        /// </summary>
        public IEnumerable<InventorySlot> GetAllItems()
        {
            foreach (var itemId in _orderedItems)
            {
                if (_items.TryGetValue(itemId, out InventorySlot slot))
                    yield return slot;
            }
        }
        
        /// <summary>
        /// Get item at specific index.
        /// </summary>
        public InventorySlot GetItemAt(int index)
        {
            if (index >= 0 && index < _orderedItems.Count)
            {
                string itemId = _orderedItems[index];
                if (_items.TryGetValue(itemId, out InventorySlot slot))
                    return slot;
            }
            return null;
        }
        
        /// <summary>
        /// Clear the entire inventory.
        /// </summary>
        public void ClearInventory()
        {
            _items.Clear();
            _orderedItems.Clear();
            OnInventoryChanged?.Invoke();
        }
        
        /// <summary>
        /// Use an item from the inventory.
        /// </summary>
        public bool UseItem(string itemId, GameObject user)
        {
            if (!_items.TryGetValue(itemId, out InventorySlot slot))
                return false;
            
            if (slot.Item.Use(user))
            {
                // Consume item on use
                if (slot.Item.ConsumeOnUse)
                {
                    RemoveItem(itemId, 1);
                }
                return true;
            }
            
            return false;
        }
    }
    
    /// <summary>
    /// Represents a slot in the inventory containing an item and its quantity.
    /// </summary>
    [Serializable]
    public class InventorySlot
    {
        public InventoryItem Item { get; private set; }
        public int Quantity { get; private set; }
        
        public InventorySlot(InventoryItem item, int quantity)
        {
            Item = item;
            Quantity = quantity;
        }
        
        public void AddQuantity(int amount)
        {
            Quantity += amount;
            if (Item.MaxStackSize > 0)
                Quantity = Mathf.Min(Quantity, Item.MaxStackSize);
        }
        
        public void RemoveQuantity(int amount)
        {
            Quantity -= amount;
        }
    }
}
