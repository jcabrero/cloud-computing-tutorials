
# Requirements

You will need to install either Git Bash or WSL. One of the two will be necessary.

In MacOS it is not needed, you will only need the terminal


# Get Kubernetes Cluster Configuration
```bash
mkdir -p ~/.kube/
sudo docker cp kubernetes:/etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown 1000:1000 ~/.kube/config
```



# Install Arkade

```bash
# Note: you can also run without `sudo` and move the binary yourself
curl -sLS https://get.arkade.dev | sudo sh

arkade --help
ark --help  # a handy alias

# Windows users with Git Bash
curl -sLS https://get.arkade.dev | sh
```

# Install Kubectl
```bash
arkade install kubectl
```

# Launch Docker Compose
Launch the command:

```bash
docker compose up
```

# Check Kubernetes is working
On a separate tab:

```bash
kubectl get nodes
```

The output should be similar to:
```bash
NAME         STATUS   ROLES                  AGE   VERSION
kubernetes   Ready    control-plane,master   38m   v1.27.9+k3s1
```


Then check that all pods are working appropriately:
```bash
kubectl get pods --all-namespaces
```

The output should be similar to:
```bash
NAMESPACE     NAME                                     READY   STATUS      RESTARTS   AGE
kube-system   local-path-provisioner-957fdf8bc-wm95p   1/1     Running     0          38m
kube-system   coredns-77ccd57875-5s8cj                 1/1     Running     0          38m
kube-system   helm-install-traefik-crd-9dc88           0/1     Completed   0          38m
kube-system   svclb-traefik-b0d172f0-v7qck             2/2     Running     0          38m
kube-system   helm-install-traefik-fg7tl               0/1     Completed   1          38m
kube-system   traefik-768bdcdcdd-82b68                 1/1     Running     0          38m
kube-system   metrics-server-648b5df564-chsdg          1/1     Running     0          38m
kube-system   svclb-flask-service-6b6ed1bf-ffcqc       1/1     Running     0          37m
```
Please check that all containres have their status in `Running` or `Completed`.

# Creating the Kubernetes image.

Then we can start with the practice. In this practice, the goal is to create a autoscalable set of lambda functions that will update their amount depending on when they are used. For that, we will use k3s as the Kubernetes engine.

First, we need to produce the image that we will use. In this case, we need to produce that. Navigate to the server directory:

```bash
cd server
```

Then, you can start by building the image and uploading it to DockerHub. Note that in this case, the name of the image is important. Here you can choose to create your own image, but keep in mind, the name will need to be replicated throughout the rest of the exercise. In my case the command is:

```bash
docker build -t jcabrero/flask-grayscale:latest .
```

Then we can upload the image to DockerHub:
```bash
# Perform docker login if not done before
docker login
# Then we can upload the image:
docker push jcabrero/flask-grayscale:latest
```

Again, note that in this case `jcabrero` corresponds to the account name in DockerHub.

# Setup Minio.

This tutorial assumes some prerequisites in Minio. You can head to [http://localhost:9000](http://localhost:9000) to get to Minio. In this case, we will need to introduce `minioadmin:minioadmin` as the username and password.

Next, we will proceed to create three things. Navigate to the Administrator->Buckets and click on Create Bucket. Type the name. This tutorial assumes the existence of two different Bucket Names:
- minio-bucket: Where the inputs of the workflow will be uploaded.
- blur-bucket: Where the results of the workflow will be introduced.


# Create Access Keys for Minio.

In MinIO, navigate to User->Access Keys. Click on Create Access Key. Note down both the access key and the secret key. For the remainder of the tutorial, we will name `ACCESS_KEY` and `SECRET_KEY` to these keys.

# Setup n8n. 

Next, we will need to setup n8n. For that, we will need to setup the workflow. 
Navigate to [http://localhost:5678](http://localhost:5678). Register using whatever credentials you choose to. 

Next, tap on the Credentials tab on the left bar. Click on Add Credentials, select S3 credentials (not AWS S3, just S3). Write the following:
- S3 Endpoint: http://minio:9000
- Location: Empty it. Nothing should be written here.
- Access Key: `ACCESS_KEY`.
- Secret Key: `SECRET_KEY`.
- Set the Force Path Style to True.

# Setup the Minio Webhook for n8n.

Next, we will move to the workflows tab. There, we will be adding a new workflow. Then, we can click on the top right corner, on the three dots and select import from file. Upload the file `workflow_kubernetes.json`. Then, select the first step, called workflow. Copy the Test URL and Production URL by clicking on those. 

1. Head to Minio. In Minio navigate to Administrator->Events. 
2. Click on Add Event Destination.
3. Select Functions -> Webhook
4. As identifier choose n8n-test for the test link and n8n-prod for the production link.
5. In endpoint, introduce the URL you copied from n8n.
6. Click on the Restart banner and Refresh the webpage (`F5`).

Do this for `n8n-prod`.

1. Next head to Administrator -> Buckets.  
2. Click on `minio-bucket` or the first bucket you created.
3. Under Events, click Subscribe to Event.
4. On ARN, first select `n8n-test`.
5. Select only PUT - Object Uploaded.

Do `1 to 5` for `n8n-prod`.


# Deploy Kubernetes Deployment.

Head back to the terminal where you installed `kubectl`.

In the file `secrets.yml` change the secret `minio-access-key` and `minio-secret-key` by the output of the following command:

```bash
echo -n "<ACCESS_KEY>" |  base64
echo -n "<SECRET_KEY>" |  base64
```

This produces the `base64` encoding which is what we need to introduce in the secrets.yml file.

Introduce the secrets to the kubernetes cluster.

```bash
kubectl apply -f secrets.yml
# OUTPUT: 
# secret/flaskapi-secrets created
kubectl apply -f flask-deployment.yml 
# OUTPUT: 
# deployment.apps/flaskapi-deployment created
# service/flask-service created
```

Next we can navigate to [http://localhost:5000](http://localhost:5000). In that link, we should check that the keys are the same we initially created.


Finally, we are going to create our automatic balancing of load. For that we execute:

```bash
kubectl apply -f flask-hpa.yml
```


Now we can check if that is working appropriately by opening two terminals.

On the first terminal, we are going to watch how many replicas there are:

```bash
kubectl get hpa --watch
```

On the second terminal, we are going to generate load:

```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://10.0.0.3:5000/cpu_test; done"
```

# Other commands needed:
```bash
docker tag flask-grayscale:latest jcabrero/flask-grayscale:latest
kubectl exec flaskapi-deployment-ddb9f7dfd-p4cts -- bash
kubectl get svc
kubectl describe pod flaskapi-deployment-ddb9f7dfd-p4cts
kubectl delete deployment flaskapi-deployment
kubectl describe hpa flaskapi-hpa
kubectl delete hpa flaskapi-hpa
```
