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
        hand.transform.rotation = Quaternion.Euler(new Vector3(data[0], data[1], data[2]));
        thumb.transform.rotation = Quaternion.Euler(new Vector3(data[3], data[4], 0));
        index.transform.rotation = Quaternion.Euler(new Vector3(data[5], data[6], 0));
        middle.transform.rotation = Quaternion.Euler(new Vector3(data[7], data[8], 0));
        ring.transform.rotation = Quaternion.Euler(new Vector3(data[9], data[10], 0));
        pinky.transform.rotation = Quaternion.Euler(new Vector3(data[11], data[12], 0));
    }
}
