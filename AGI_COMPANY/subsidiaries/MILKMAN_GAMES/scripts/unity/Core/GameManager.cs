using UnityEngine;
using System;

namespace DaVerse.Core
{
    /// <summary>
    /// Singleton GameManager - Central hub for game state and cross-system communication.
    /// </summary>
    public class GameManager : MonoBehaviour
    {
        public static GameManager Instance { get; private set; }
        
        [Header("Game State")]
        [SerializeField] private GameState currentState = GameState.MainMenu;
        
        [Header("Systems")]
        [SerializeField] private SceneLoader sceneLoader;
        [SerializeField] private InputManager inputManager;
        [SerializeField] private AudioManager audioManager;
        
        public GameState CurrentState => currentState;
        
        public event Action<GameState> OnGameStateChanged;
        public event Action OnGamePaused;
        public event Action OnGameResumed;
        public event Action OnGameQuit;
        
        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            
            Instance = this;
            DontDestroyOnLoad(gameObject);
            InitializeSystems();
        }
        
        private void InitializeSystems()
        {
            if (sceneLoader == null) sceneLoader = gameObject.AddComponent<SceneLoader>();
            if (inputManager == null) inputManager = gameObject.AddComponent<InputManager>();
            if (audioManager == null) audioManager = gameObject.AddComponent<AudioManager>();
        }
        
        public void SetGameState(GameState newState)
        {
            if (currentState == newState) return;
            
            var previousState = currentState;
            currentState = newState;
            
            HandleStateTransition(previousState, newState);
            OnGameStateChanged?.Invoke(newState);
        }
        
        private void HandleStateTransition(GameState from, GameState to)
        {
            switch (to)
            {
                case GameState.Paused:
                    Time.timeScale = 0f;
                    OnGamePaused?.Invoke();
                    break;
                case GameState.Playing:
                    Time.timeScale = 1f;
                    OnGameResumed?.Invoke();
                    break;
                case GameState.Quitting:
                    OnGameQuit?.Invoke();
                    break;
            }
        }
        
        public void PauseGame() => SetGameState(GameState.Paused);
        public void ResumeGame() => SetGameState(GameState.Playing);
        public void QuitGame() => SetGameState(GameState.Quitting);
        
        private void OnApplicationQuit()
        {
            SetGameState(GameState.Quitting);
        }
    }
    
    public enum GameState
    {
        MainMenu,
        Loading,
        Playing,
        Paused,
        GameOver,
        Victory,
        Quitting
    }
}
