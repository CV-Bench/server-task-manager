copy () {
    sudo cp $1 $2
}

replace() {
    sudo sed -i 's,'$1','$2',' $3
}

pythonpath=$(which python)

cv_backend_service_result_path=/etc/systemd/system/cv-backend.service

copy cv-backend.service $cv_backend_service_result_path

replace '<WorkDir>' $PWD $cv_backend_service_result_path
replace '<PythonDir>' $pythonpath $cv_backend_service_result_path

# Start Services

sudo systemctl daemon-reload

sudo systemctl start cv-backend.service

sudo systemctl enable cv-backend.service