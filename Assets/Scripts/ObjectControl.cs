using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectControl : MonoBehaviour
{
    public GameObject hand, palm, thumb, index, middle, ring, pinky;

    // Start is called before the first frame update
    void Start()
    {
        hand = GameObject.Find("Hand_control");
        palm = GameObject.Find("Palm_fcontrol");
        thumb = GameObject.Find("Thumb_control");
        index = GameObject.Find("Index_control");
        middle = GameObject.Find("Middle_control");
        ring = GameObject.Find("Ring_control");
        pinky = GameObject.Find("Pinky_control");
    }

    // Update is called once per frame
    void Update()
    {
    }

    public void Modify(float[] data)
    {
        hand.transform.rotation = Quaternion.Euler(new Vector3(data[0], data[1], 0));
        thumb.transform.rotation = Quaternion.Euler(new Vector3(0, data[2], 0));
        index.transform.rotation = Quaternion.Euler(new Vector3(0, data[3], 0));
        middle.transform.rotation = Quaternion.Euler(new Vector3(0, data[4], 0));
        ring.transform.rotation = Quaternion.Euler(new Vector3(0, data[5], 0));
        pinky.transform.rotation = Quaternion.Euler(new Vector3(0, data[6], 0));
    }

    public void ModifyForDots(float[] data)
    {
        for (int i = 0; i < 11; i++)
        {
            string name;
            if (i == 0) name = "landmark";
            else name = "landmark (" + i + ")";
            GameObject.Find(name).transform.position = new Vector3(data[i * 3], data[i * 3 + 1], -data[i * 3 + 2]);
        }
    }
}
