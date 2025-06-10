using UnityEngine;

public class Heart : MonoBehaviour
{

    public Sprite OnHeart;
    public Sprite OffHeart;

    // 몇 번째 생명 오브젝트인지?
    public int LiveNumber;

    // * Sprite를 화면에 그려주는 역할을 함 
    public SpriteRenderer SpriteRenderer;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(GameRunManager.Instance.Lives >= LiveNumber)
        {
            SpriteRenderer.sprite = OnHeart;
        }
        else
        {
            SpriteRenderer.sprite = OffHeart;
        }
    }
}
