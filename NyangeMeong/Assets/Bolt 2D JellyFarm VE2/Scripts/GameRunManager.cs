using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public enum GameState
{
    Intro,
    Playing,
    Dead
}

public class GameRunManager : MonoBehaviour
{
    public static GameRunManager Instance;

    public GameState State = GameState.Intro;

    public int Lives = 3;

    [Header("References")]
    public GameObject IntroUI;
    public GameObject DeadUI;
    public GameObject EnemySpawner;
    public GameObject FoodSpawner;
    public GameObject GoldenSpawner;

    public Player PlayerScript;
    public TMP_Text scoreText;

    public GameObject RestartButton;

    // ✅ 점수 누적용 변수
    private float accumulatedScore = 0f;

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        IntroUI.SetActive(true);

        if (RestartButton != null)
            RestartButton.SetActive(false);
    }

    public float CalculateGameSpeed()
    {
        if (State != GameState.Playing)
        {
            return 5f;
        }

        float speed = 8f + (0.5f * Mathf.Floor(accumulatedScore / 10f));
        return Mathf.Min(speed, 30f);
    }

    void Update()
    {
        // ✅ 점수 누적
        if (State == GameState.Playing)
        {
            accumulatedScore += Time.deltaTime;
            scoreText.text = "Score: " + Mathf.FloorToInt(accumulatedScore);
        }

        // 게임 시작
        if (State == GameState.Intro && Input.GetKeyDown(KeyCode.Space))
        {
            State = GameState.Playing;
            IntroUI.SetActive(false);

            EnemySpawner.SetActive(true);
            FoodSpawner.SetActive(true);
            GoldenSpawner.SetActive(true);

            accumulatedScore = 0f; // ✅ 점수 초기화
        }

        // 사망 처리
        if (State == GameState.Playing && Lives == 0)
        {
            PlayerScript.KillPlayer();

            EnemySpawner.SetActive(false);
            FoodSpawner.SetActive(false);
            GoldenSpawner.SetActive(false);

            State = GameState.Dead;
            DeadUI.SetActive(true);

            if (RestartButton != null)
                RestartButton.SetActive(true);
        }
    }

    public void OnClickRestart()
    {
        SceneManager.LoadScene("main");
    }
}
