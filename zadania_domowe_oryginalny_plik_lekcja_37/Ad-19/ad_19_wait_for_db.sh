#!/bin/sh
set -e

echo "[INIT] Czekam az baza danych bedzie dostepna..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
    echo "[INIT] Baza jeszcze niedostepna, czekam 2s..."
    sleep 2
done

echo "[INIT] Baza dostepna."