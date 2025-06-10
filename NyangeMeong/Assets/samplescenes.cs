using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class samplescenes : MonoBehaviour
{
    public void SamplescenesCtrl()
    {
        SceneManager.LoadScene("SampleScene"); // 이동하는 신
        Debug.Log("Main Scenes Go");
    }

}
