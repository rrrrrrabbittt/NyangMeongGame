using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameScenesMove : MonoBehaviour
{
    public void GameScenesCtrl()
    {
        SceneManager.LoadScene("main"); // 이동하는 신
        Debug.Log("Main Scenes Go");
    }

}
