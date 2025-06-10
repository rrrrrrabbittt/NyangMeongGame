using UnityEngine;
using UnityEngine.SceneManagement;

public class JellyController : MonoBehaviour
{
    private SpriteRenderer sr;

    void Awake()
    {
        sr = GetComponentInChildren<SpriteRenderer>();
        Debug.Log("Awake - SpriteRenderer 연결됨: " + (sr != null));
    }

    void Start()
    {
        SceneManager.sceneLoaded += OnSceneLoaded;
        Debug.Log("Start - 현재 씬: " + SceneManager.GetActiveScene().name);
        CheckVisibility();
    }

    void OnDestroy()
    {
        SceneManager.sceneLoaded -= OnSceneLoaded;
    }

    void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        Debug.Log("씬 로드됨: " + scene.name);
        CheckVisibility();
    }

    void CheckVisibility()
    {
        string currentScene = SceneManager.GetActiveScene().name;
        Debug.Log("CheckVisibility - 현재 씬 이름: " + currentScene);
        sr.enabled = (currentScene == "SampleScene");
    }
}
