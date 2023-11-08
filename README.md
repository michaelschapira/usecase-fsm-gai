# Highleve steps

1. login to ocp on the command line
2. login to the registry via podman login
3. build
4. tag
5. push image
6. create a new app in OCP using the imagestream 

> Note: each time image is updated, pod gets recycled to use new image. 

# Commands

podman login -u ocpadmin -p sha256~ZWN2wn-RrsruOMYeEZEVPf5Mya0KRmg70xVsQVS_8DY internal-registry-openshift-image-registry.apps.cpd47fsm2.tec.ihost.com
podman build --no-cache -t gai-usecase:v1 .
podman tag localhost/gai-usecase:v1 internal-registry-openshift-image-registry.apps.cpd47fsm2.tec.ihost.com/fsm-apps/gai-usecase:20231108 
podman push --tls-verify=false internal-registry-openshift-image-registry.apps.cpd47fsm2.tec.ihost.com/fsm-apps/gai-usecase:20231108
