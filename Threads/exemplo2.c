#include<stdio.h>
#include<pthread.h>
#define N 20

struct var_t{

	long x;
	char c;

};

//Deve ser declarado como ponteiro para função
void *hello(void *i){

	long id;
	char c;
	struct var_t *y;

	y=(struct var_t *)i;

	id=y->x;
	c=y->c;

	printf("Olá, sou a thread %ld e recebi o caracter %c\n", id, c);

	pthread_exit(NULL);

}


int main(){

	pthread_t threads[N]; //handlers das threads
	long i;
	struct var_t x[N];

	for(i=0;i<N;i++){
		x[i].c=(char)(i+32);
		x[i].x=i;
		printf("Criando thread %ld\n", i);
		//(handler, atributos, função a ser executada, parâmetro da função)
		pthread_create(&threads[i],NULL,&hello,(void *)&x[i]);
	}

	//Deve ser chamada para sincronizar as threads no final
	for(i=0;i<N;i++){
		pthread_join(&threads[i],NULL);
	}

	pthread_exit(NULL);

}
