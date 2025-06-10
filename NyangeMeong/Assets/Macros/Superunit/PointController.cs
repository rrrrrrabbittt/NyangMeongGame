using UnityEngine;

public class PointController : MonoBehaviour
{
    RaycastHit hit;
    Animator anim;
    
    void Awake()
    {
        anim = GetComponent<Animator>();
    }

    public void MyDrag()
    {
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition); // 마우스 위치에서 레이 생성
        if (Physics.Raycast(ray, out hit, Camera.main.farClipPlane, LayerMask.GetMask("Floor"))) { // Floor 오브젝트에 레이캐스팅
            Vector3 nextPos = hit.point; // 바닥에 닿은 위치
            nextPos.y = 0.5f;
            transform.position = Vector3.Lerp(transform.position, nextPos, 0.2f); // 얻은 위치로 이동
        }
        anim.SetBool("isDrag", true);
    }

    public void MyDrop()
    {
        transform.Translate(Vector3.down * 0.5f);
        anim.SetBool("isDrag", false);
    }
}
