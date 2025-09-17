#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

sem_t mutex;
sem_t write_lock;
int read_count = 0;

int shared_variable = 0;

void* reader(void* arg) {
    int id = *(int*)arg;

    sem_wait(&mutex);
    if (++read_count == 1) {
        sem_wait(&write_lock);
    }
    sem_post(&mutex);

    printf("Read value '%d' from reader %d\n", shared_variable, id);

    sem_wait(&mutex);
    if (--read_count == 0) {
        sem_post(&write_lock);
    }
    sem_post(&mutex);

    return NULL;
}

void* writer(void* arg) {
    int id = *(int*)arg;

    sem_wait(&write_lock);

    shared_variable += 5;
    printf("Writing value %d\n", shared_variable);

    sem_post(&write_lock);

    return NULL;
}

int main() {
    sem_init(&mutex, 0, 1);
    sem_init(&write_lock, 0, 1);

    pthread_t readers[5], writers[5];
    int ids[5] = {1, 2, 3, 4, 5};

    for (int i = 0; i < 5; i++) {
        pthread_create(&writers[i], NULL, writer, &ids[i]);
        pthread_create(&readers[i], NULL, reader, &ids[i]);
    }

    for (int i = 0; i < 5; i++) {
        pthread_join(readers[i], NULL);
        pthread_join(writers[i], NULL);
    }

    sem_destroy(&mutex);
    sem_destroy(&write_lock);

    return 0;
}
