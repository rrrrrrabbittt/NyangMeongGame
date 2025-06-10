using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameSceneMove : MonoBehaviour
{

    public void GameScnesCtrl() {
        SceneManager.LoadScene("Game Scene"); // 어떤 씬 이름으로 이동할건지
    }

}
