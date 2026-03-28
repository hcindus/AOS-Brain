using System;
using System.Collections.Generic;

namespace DaVerse.Core
{
    /// <summary>
    /// Decoupled event system for cross-system communication.
    /// </summary>
    public static class EventBus
    {
        private static Dictionary<Type, Delegate> _events = new Dictionary<Type, Delegate>();
        
        public static void Subscribe<T>(Action<T> handler) where T : IGameEvent
        {
            var eventType = typeof(T);
            if (_events.ContainsKey(eventType))
                _events[eventType] = Delegate.Combine(_events[eventType], handler);
            else
                _events[eventType] = handler;
        }
        
        public static void Unsubscribe<T>(Action<T> handler) where T : IGameEvent
        {
            var eventType = typeof(T);
            if (_events.ContainsKey(eventType))
            {
                _events[eventType] = Delegate.Remove(_events[eventType], handler);
                if (_events[eventType] == null)
                    _events.Remove(eventType);
            }
        }
        
        public static void Publish<T>(T eventData) where T : IGameEvent
        {
            var eventType = typeof(T);
            if (_events.TryGetValue(eventType, out var handler))
                (handler as Action<T>)?.Invoke(eventData);
        }
        
        public static void Clear()
        {
            _events.Clear();
        }
    }
    
    public interface IGameEvent { }
    
    // Common game events
    public struct PlayerSpawnedEvent : IGameEvent { public PlayerController Player; }
    public struct PlayerDiedEvent : IGameEvent { }
    public struct ItemCollectedEvent : IGameEvent { public string ItemId; public int Quantity; }
    public struct LevelCompletedEvent : IGameEvent { public string LevelName; }
    public struct SceneChangedEvent : IGameEvent { public string SceneName; }
    public struct QuestStartedEvent : IGameEvent { public string QuestId; }
    public struct QuestCompletedEvent : IGameEvent { public string QuestId; }
}
