#!/bin/bash

# Tuer tegrastats
if [ -f /tmp/tegrastats_pid.txt ]; then
    TEGRASTATS_PID=$(cat /tmp/tegrastats_pid.txt)
    echo "Tentative d'arrêt de TegraStats avec le PID : $TEGRASTATS_PID"
    kill $TEGRASTATS_PID 2>/dev/null
    sleep 1
    if [ -n "$TEGRASTATS_PID" ] && ps -p $TEGRASTATS_PID > /dev/null; then
        echo "TegraStats n'a pas répondu, utilisation de kill -9"
        kill -9 $TEGRASTATS_PID
    fi
    rm /tmp/tegrastats_pid.txt
else
    echo "Fichier PID de TegraStats non trouvé."
fi

# Tuer la boucle tail | while
if [ -f /tmp/loop_pid.txt ]; then
    LOOP_PID=$(cat /tmp/loop_pid.txt)
    echo "Tentative d'arrêt de la boucle avec le PID : $LOOP_PID"
    kill $LOOP_PID 2>/dev/null
    sleep 1
    if [ -n "$LOOP_PID" ] && ps -p $LOOP_PID > /dev/null; then
        echo "La boucle n'a pas répondu, utilisation de kill -9"
        kill -9 $LOOP_PID
    fi
    rm /tmp/loop_pid.txt
else
    echo "Fichier PID de la boucle non trouvé."
fi

# Nettoyer le log
rm -f /tmp/outxx.txt
echo "Nettoyage terminé."
