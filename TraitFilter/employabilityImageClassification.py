import tensorflow as tf
import numpy as np
import random

def sigmoid(z):
    return 1.0/(1.0 + tf.exp(-z))
def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

class Network(object):

    def __init__(self,layers):
        self.num_layers = len(layers)
        self.layers = layers
        self.weights = [tf.random_normal(shape = [x,y],stddev=0.4,dtype='float32') for x,y in zip(layers[:-1],layers[1:])]
        self.biases = [tf.random_normal(shape = [1,y], stddev=0.4,dtype='float32') for y in layers[1:]]

    def feedforward(self,inp):
       for bias,weight in zip(self.biases,self.weights):
            inp = sigmoid(tf.add(tf.matmul(inp,weight),bias))
       return inp

    def stochastic_gradient_descent(self,training_data,batch_size,epochs,rate,test_data = None):
        n = len(training_data)
        for epoch in range(epochs):
            random.shuffle(training_data)
            batches = [training_data[i:i+batch_size] for i in range(0,n,batch_size)]
            
            for batch in batches:
                b_differential = [tf.zeros(shape=bias.get_shape(),dtype='float32',name='nabla_b') for bias in self.biases]
                w_differential = [tf.zeros(shape=weight.get_shape(),dtype='float32',name='nabla_w') for weight in self.weights]

                for inp,out in batch:
                    d_b_differential, d_w_differential = self.backpropagation(inp,out)
                    b_differential = [i+j for i,j in zip(b_differential, d_b_differential)]                
                    w_differential = [i+j for i,j in zip(w_differential, d_w_differential)]
                    
                self.weights = [w-(rate/len(batch))*(nw) for w, nw in zip(self.weights,w_differential)]
                self.biases = [b-(rate/len(batch))*(bw) for b, bw in zip(self.biases,b_differential)]

            if test_data:
                test_count = len(test_data)
            if test_data:
                print('Epoch #:',epoch,'accurate to:',self.evaluate(test_data),'/',test_count)
            else:
                print('Epoch #:',epoch,'done')

    def backpropagation(self,x,y):
        b_differential = [tf.zeros(shape=bias.get_shape(),dtype='float32',name='nabla_b') for bias in self.biases]
        w_differential = [tf.zeros(shape=weight.get_shape(),dtype='float32',name='nabla_w') for weight in self.weights]
        activation = x
        activations = [x]
        raw_activs = []
        
        for bias,weight in zip(self.biases,self.weights):
            raw_activ = tf.matmul(activation,weight)
            raw_activs.append(raw_activ)
            activation = sigmoid(raw_activ)
            activations.append(activation)

        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(raw_activs[-1])
        b_differential[-1] = delta
        w_differential[-1] = tf.matmul(delta, tf.transpose(activations[-2]))
        
        for i in range(2,self.num_layers):
            raw_activ = raw_activs[-i]
            delta = tf.matmul(tf.transpose(delta,self.weights[1-i]))*sigmoid_prime(raw_activ)
            b_differential[-i] = delta
            w_differential[-i] = tf.matmul(delta,tf.transpose(activations[-1-i]))
            
        return (b_differential,w_differential)
        
        
    def eval(self,test_data):
        test_results = [(tf.argmax(self.feedforward(x)),y) for x,y in test_data]
        return sum(int(x==y) for (x,y) in test_results)
            
    def cost_derivative(self,output_activations,y):
        return output_activations-y
        

out = [1,0,0,0,0,0,0]

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    net = Network([2,3,4])
    print(sess.run([net.stochastic_gradient_descent([([[0.0,1.0]],[[1.0,2.0,3.0,4.0]])],1,1,0.001)],feed_dict = {}))






