import roslibpy
import yaml


def load_field_map(path: str) -> dict:
    """Load the YAML mapping file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


class DynamicSubscriberManager:
    """
    Creates ROSLIBPY topic subscribers based on a simple YAML field map.
    Example YAML:
        odom:
          pose_x: "pose.pose.position.x"
          pose_y: "pose.pose.position.y"
    """

    def __init__(self, ros: roslibpy.Ros, sensor_data, prefix: str):
        self.ros = ros
        self.sensor_data = sensor_data
        self.prefix = prefix.rstrip("/")
        self.subs = {}

    def register_from_yaml(self, yaml_path: str):
        cfg = load_field_map(yaml_path)

        for topic_name, mapping in cfg.items():
            full_topic = f"{self.prefix}/{topic_name}"
            # msg_type = self.ros.get_topic_type(full_topic)
            msg_type = mapping.pop("__type__", None) or self.ros.get_topic_type(full_topic)

            if not msg_type:
                print(f"[WARN] Could not determine message type for {full_topic}. Skipping.")
                continue

            topic = roslibpy.Topic(self.ros, full_topic, msg_type)
            topic.subscribe(lambda msg, m=mapping: self._update(msg, m))
            self.subs[topic_name] = topic
            print(f"[OK] Subscribed to {full_topic} ({msg_type})")

    # def _update(self, msg: dict, mapping: dict):
    #     for attr, path_str in mapping.items():
    #         try:
    #             val = msg
    #             for key in path_str.split("."):
    #                 val = val[key]
    #             setattr(self.sensor_data, attr, val)
    #         except (KeyError, TypeError):
    #             continue
    def _update(self, msg: dict, mapping: dict):
        for attr, path_cfg in mapping.items():
            try:
                if isinstance(path_cfg, dict):
                    path = path_cfg["path"]
                    val = msg
                    for key in path.split("."):
                        val = val[key]
                    if "index" in path_cfg and isinstance(val, (list, tuple)):
                        val = val[path_cfg["index"]]
                else:
                    # Plain dotted path
                    val = msg
                    for key in path_cfg.split("."):
                        val = val[key]
                setattr(self.sensor_data, attr, val)
            except (KeyError, TypeError, IndexError):
                continue
