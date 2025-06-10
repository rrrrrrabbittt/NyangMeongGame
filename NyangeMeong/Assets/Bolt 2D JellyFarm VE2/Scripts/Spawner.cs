using UnityEngine;

public class Spawner : MonoBehaviour
{

    [Header("Settings")]
    public float minSpawnDelay;
    public float maxSpawnDelay;


    [Header("References")]
    public GameObject[] gameObjects;

    
    // * OnEnable() : 오브젝트가 활성화될 때마다 호출되는 메서드 
    void OnEnable()
    {
        // Random 범위 초후에 Spawn 함수 실행 
        Invoke("Spawn", Random.Range(minSpawnDelay,maxSpawnDelay));
    }

    void OnDisable()
    {
        CancelInvoke();
    }

    void Spawn(){
        // 랜덤 오브젝트 선택
        GameObject randomObject = gameObjects[Random.Range(0, gameObjects.Length)];
        // 위 오브젝트를 인스턴스화 해서 씬에다가 올려 놓음 
        Instantiate(randomObject,transform.position, Quaternion.identity);

        // Random 범위 초후에 Spawn 함수 실행 
        Invoke("Spawn", Random.Range(minSpawnDelay,maxSpawnDelay));
    }
}
