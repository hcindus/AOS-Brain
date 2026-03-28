using UnityEngine;

namespace DaVerse.Inventory
{
    /// <summary>
    /// ScriptableObject for defining inventory items.
    /// </summary>
    [CreateAssetMenu(fileName = "New Item", menuName = "DaVerse/Inventory/Item")]
    public class InventoryItem : ScriptableObject
    {
        [Header("Basic Info")]
        [SerializeField] private string itemId;
        [SerializeField] private string displayName;
        [TextArea]
        [SerializeField] private string description;
        
        [Header("Visuals")]
        [SerializeField] private Sprite icon;
        [SerializeField] private GameObject worldPrefab;
        
        [Header("Stacking")]
        [SerializeField] private bool isStackable = true;
        [SerializeField] private int maxStackSize = 99;
        
        [Header("Usage")]
        [SerializeField] private bool consumable = true;
        [SerializeField] private bool consumeOnUse = true;
        [SerializeField] private ItemEffect[] effects;
        
        [Header("Value")]
        [SerializeField] private int buyPrice;
        [SerializeField] private int sellPrice;
        
        [Header("Rarity")]
        [SerializeField] private ItemRarity rarity = ItemRarity.Common;
        
        [Header("Category")]
        [SerializeField] private ItemCategory category = ItemCategory.Misc;
        
        // Properties
        public string ItemId => string.IsNullOrEmpty(itemId) ? name : itemId;
        public string DisplayName => displayName;
        public string Description => description;
        public Sprite Icon => icon;
        public GameObject WorldPrefab => worldPrefab;
        public bool IsStackable => isStackable;
        public int MaxStackSize => maxStackSize;
        public bool Consumable => consumable;
        public bool ConsumeOnUse => consumeOnUse;
        public int BuyPrice => buyPrice;
        public int SellPrice => sellPrice;
        public ItemRarity Rarity => rarity;
        public ItemCategory Category => category;
        
        /// <summary>
        /// Use the item and apply its effects.
        /// </summary>
        public virtual bool Use(GameObject user)
        {
            if (!consumable) return false;
            
            bool used = false;
            foreach (var effect in effects)
            {
                if (effect != null && effect.Apply(user))
                {
                    used = true;
                }
            }
            
            return used;
        }
        
        /// <summary>
        /// Get the display color based on rarity.
        /// </summary>
        public Color GetRarityColor()
        {
            return rarity switch
            {
                ItemRarity.Common => Color.white,
                ItemRarity.Uncommon => Color.green,
                ItemRarity.Rare => Color.blue,
                ItemRarity.Epic => Color.magenta,
                ItemRarity.Legendary => new Color(1f, 0.5f, 0f), // Orange
                ItemRarity.Unique => Color.red,
                _ => Color.white
            };
        }
        
        private void OnValidate()
        {
            if (string.IsNullOrEmpty(itemId))
                itemId = name;
            
            if (string.IsNullOrEmpty(displayName))
                displayName = name;
        }
    }
    
    public enum ItemRarity
    {
        Common,
        Uncommon,
        Rare,
        Epic,
        Legendary,
        Unique
    }
    
    public enum ItemCategory
    {
        Weapon,
        Armor,
        Consumable,
        Material,
        KeyItem,
        QuestItem,
        Misc
    }
}
