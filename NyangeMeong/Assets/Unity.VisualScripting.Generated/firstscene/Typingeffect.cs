using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class TypingEffect : MonoBehaviour
{
    public Text tx;
    private string m_text = "저는 처음엔 박스 안에 담겨 있었어요. \n며칠 동안 아무도 오지 않아서,\n너무 무서웠는데... \n절 데려와주셔서 감사해요.\n이젠 행복할 수 있을까요? ";

    void Start()
    {
        StartCoroutine(_typing());
    }

    IEnumerator _typing()
    {
        yield return new WaitForSeconds(2f);
        for (int i = 0; i <= m_text.Length; i++)
        {
            tx.text = m_text.Substring(0, i);
            yield return new WaitForSeconds(0.15f);
        }
    }
}
