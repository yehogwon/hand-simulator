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
        int delta = 3;
        GameObject.Find("landmark").transform.position = new Vector3(data[0], -data[1] + delta, data[2]);
        GameObject.Find("landmark (1)").transform.position = new Vector3(data[3], -data[4] + delta, data[5]);
        GameObject.Find("landmark (2)").transform.position = new Vector3(data[6], -data[7] + delta, data[8]);
        GameObject.Find("landmark (3)").transform.position = new Vector3(data[9], -data[10] + delta, data[11]);
        GameObject.Find("landmark (4)").transform.position = new Vector3(data[12], -data[13] + delta, data[14]);
        GameObject.Find("landmark (5)").transform.position = new Vector3(data[15], -data[16] + delta, data[17]);
        GameObject.Find("landmark (6)").transform.position = new Vector3(data[18], -data[19] + delta, data[20]);
        GameObject.Find("landmark (7)").transform.position = new Vector3(data[21], -data[22] + delta, data[23]);
        GameObject.Find("landmark (8)").transform.position = new Vector3(data[24], -data[25] + delta, data[26]);
        GameObject.Find("landmark (9)").transform.position = new Vector3(data[27], -data[28] + delta, data[29]);
        GameObject.Find("landmark (10)").transform.position = new Vector3(data[30], -data[31] + delta, data[32]);
        GameObject.Find("landmark (11)").transform.position = new Vector3(data[33], -data[34] + delta, data[35]);
        GameObject.Find("landmark (12)").transform.position = new Vector3(data[36], -data[37] + delta, data[38]);
        GameObject.Find("landmark (13)").transform.position = new Vector3(data[39], -data[40] + delta, data[41]);
        GameObject.Find("landmark (14)").transform.position = new Vector3(data[42], -data[43] + delta, data[44]);
        GameObject.Find("landmark (15)").transform.position = new Vector3(data[45], -data[46] + delta, data[47]);
        GameObject.Find("landmark (16)").transform.position = new Vector3(data[48], -data[49] + delta, data[50]);
        GameObject.Find("landmark (17)").transform.position = new Vector3(data[51], -data[52] + delta, data[53]);
        GameObject.Find("landmark (18)").transform.position = new Vector3(data[54], -data[55] + delta, data[56]);
        GameObject.Find("landmark (19)").transform.position = new Vector3(data[57], -data[58] + delta, data[59]);
        GameObject.Find("landmark (20)").transform.position = new Vector3(data[60], -data[61] + delta, data[62]);
    }
}
