import os

import pulumi
import pulumi_eks as eks
from pulumi_eks import ClusterNodeGroupOptionsArgs


def read_my_key(name="id_rsa.pub"):
    with open(f'{os.getenv("HOME")}/.ssh/{name}', "r") as f:
        key = f.read()
    return key


startup_script = """
    """


def create_cluster(name):
    # Create an EKS cluster.
    cluster = eks.Cluster(
        f"{name}",
        public_access_cidrs=["0.0.0.0/0"],
        node_group_options=ClusterNodeGroupOptionsArgs(
            instance_type="t4g.small",
            desired_capacity=2,
            min_size=1,
            max_size=5,
            node_associate_public_ip_address=True,
            # node_user_data=startup_script,
            node_public_key=read_my_key(),
        ),
        enabled_cluster_log_types=[],
    )
    
    pulumi.export(f"kubeconfig-{name}", cluster.kubeconfig)


create_cluster("small-test")
