import kopf
import logging
from methods.k8s import KubernetesHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


@kopf.on.create('rocketapis')
def create_handler(spec, name, namespace, logger, **kwargs):
    k8s_handler = KubernetesHandler(logger=logger, namespace=namespace)
    k8s_handler.create_deployment(spec, name)
    k8s_handler.create_service(spec, name)

@kopf.on.update('rocketapis')
def update_handler(spec, name, namespace, logger, **kwargs):
    k8s_handler = KubernetesHandler(logger=logger, namespace=namespace)
    k8s_handler.update_deployment(spec, name)
    k8s_handler.update_service(spec, name)

@kopf.on.delete('rocketapis')
def delete_handler(spec, name, namespace, logger, **kwargs):
    k8s_handler = KubernetesHandler(logger=logger, namespace=namespace)
    k8s_handler.delete_resources(name)

    