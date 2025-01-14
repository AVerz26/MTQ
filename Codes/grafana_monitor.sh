#!/bin/bash

MYSQL_USER="mantiqueira"
MYSQL_PASSWORD="mantiqueira"
MYSQL_HOST="localhost"
MYSQL_DATABASE="grafana_data"

while true; do

    from_time=$(date --utc +"%Y-%m-%dT03:00:00.001Z")
    to_time=$(date --utc +"%Y-%m-%dT%H:%M:%S.001Z")
    echo "from_time: $from_time"
    echo "to_time: $to_time"
    curl -H "Authorization: Bearer glsa_8c5USWBApy9HRJPUfXV8ZNOGXnuQWrG2_d5e0b6af" "http://localhost:3000/render/d-solo/bdwaaenz6l8g0d?orgId=1&from=${from_time}&to=${to_time}&timezone=browser&refresh=3m&viewPanel=panel-16&panelId=panel-16&__feature.dashboardSceneSolo&width=1000&height=500&tz=America%2FCuiaba" -o ./grafana_images/grafico.png    
    curl -H "Authorization: Bearer glsa_8c5USWBApy9HRJPUfXV8ZNOGXnuQWrG2_d5e0b6af" "http://localhost:3000/render/d-solo/bdwaaenz6l8g0d?orgId=1&from=${from_time}&to=${to_time}&timezone=browser&refresh=3m&panelId=panel-6&__feature.dashboardSceneSolo&width=250&height=250&tz=America%2FCuiaba" -o ./grafana_images/aca.png   
    curl -H "Authorization: Bearer glsa_8c5USWBApy9HRJPUfXV8ZNOGXnuQWrG2_d5e0b6af" "http://localhost:3000/render/d-solo/bdwaaenz6l8g0d?orgId=1&from=${from_time}&to=${to_time}&timezone=browser&refresh=3m&viewPanel=panel-13&panelId=panel-13&__feature.dashboardSceneSolo&width=800&height=900&tz=America%2FCuiaba" -o ./grafana_images/caixas.png   
    curl -H "Authorization: Bearer glsa_8c5USWBApy9HRJPUfXV8ZNOGXnuQWrG2_d5e0b6af" "http://localhost:3000/render/d-solo/bdwaaenz6l8g0d?orgId=1&from=${from_time}&to=${to_time}&timezone=browser&refresh=3m&viewPanel=panel-1&panelId=panel-1&__feature.dashboardSceneSolo&width=1000&height=500&tz=America%2FCuiaba" -o ./grafana_images/aca_moba.png
    curl -H "Authorization: Bearer glsa_8c5USWBApy9HRJPUfXV8ZNOGXnuQWrG2_d5e0b6af" "http://localhost:3000/render/d-solo/bdwaaenz6l8g0d?orgId=1&from=${from_time}&to=${to_time}&timezone=browser&refresh=3m&viewPanel=panel-8&panelId=panel-8&__feature.dashboardSceneSolo&width=300&height=150&tz=America%2FCuiaba" -o ./grafana_images/hora.png
    
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    sudo ss -tnp | grep 'grafana' | awk '{print $5}' | sort | uniq | while read ip; do    
        clean_ip=$(echo $ip | sed -e 's/::ffff://g' -e 's/\([0-9]*\.[0-9]*\.[0-9]*\.[0-9]*\).*/\1/')
        
        
        mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" "$MYSQL_DATABASE" -e \
            "INSERT INTO grafana_ips (timestamp, ip_address) VALUES ('$timestamp', '$clean_ip');"
    done
    
    sleep 120
done