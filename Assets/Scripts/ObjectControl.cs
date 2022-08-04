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
        Transform t = pinky.transform;
        pinky.transform.rotation = Quaternion.Euler(new Vector3(25, 50, 0));
    }
}
