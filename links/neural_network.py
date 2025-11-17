import numpy as np
import warnings
import sys

class Layer:

    def __init__(self,num_nodes_in,num_nodes_out):
        # How many nodes are coming in this layer and how many nodes are leaving this layer
        self.num_nodes_in=num_nodes_in
        self.num_nodes_out=num_nodes_out

        # Weights and biases initialised, these adjust the decision bar
        self.weights=(np.random.standard_normal((num_nodes_in,num_nodes_out))/num_nodes_in**0.5).flatten()
        self.biases=np.zeros(num_nodes_out)
        self.inputs=np.zeros(num_nodes_in) # Weights from the incoming nodes

        # Needed for the regularization
        self.weight_velocities=np.zeros(len(self.weights))
        self.bias_velocities=np.zeros(num_nodes_out)

        # Store the number needed for the gradient to be 0
        self.cost_gradient_w=np.zeros(len(self.weights))
        self.cost_gradient_b=np.zeros(num_nodes_out)
    

    @staticmethod
    def activation(weighted_input): # Bend or changes the shape of the decision bar
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('error')

                #return weighted_input # Linear
                return 1/(1+np.exp(-weighted_input)) # Sigmoid
                #return np.tanh(weighted_input) # TanH
                #return np.maximum(0,weighted_input) # Relu
        
        except RuntimeWarning:
            print('Overflow!!')
            sys.exit()
    

    def calculate_outputs(self,input):
        self.weighted_inputs=[]
        self.activations=[]
        self.inputs=input

        # Does the operation, weighted input of a node = input*weight (of all the incoming nodes) + bias (of this node)
        for i in range(self.num_nodes_out):
            weighted_input=self.biases[i]

            for j in range(self.num_nodes_in):
                weighted_input+=input[j]*self.weights[i*self.num_nodes_in+j]

            self.weighted_inputs.append(weighted_input)


        # Puts the result through the activation function
        for i in range(len(self.weighted_inputs)):
            self.activations.append(self.activation(self.weighted_inputs[i]))
        #print(self.activations)

        return self.activations
    

    def activation_derivative(self,weighted_input): # The derivative of the activation (used to bend or change the shape of the decision bar)
        #return 1 # Linear
        return weighted_input*(1-weighted_input) # Sigmoid
        #return 1-np.tanh(weighted_input)**2 # TanH
        #return np.where(weighted_input>0,1,0) # ReLU


    @staticmethod
    def node_cost_derivative(output,expected_outcome): # The derivative of the equation that calculates how much is the loss
        return 2*(output-expected_outcome)
    

    def calculate_output_layer_node_values(self,expected_outputs):
        node_values=np.zeros(self.num_nodes_out)

        for i in range(len(node_values)): # For each node in the output layer
            activation_derivative=self.activations[i]
            cost_derivative=self.node_cost_derivative(self.activations[i],expected_outputs[i])

            node_values[i]=activation_derivative*cost_derivative # This is the operation that calculates how sensitive the loss is to the inputs of the neural network

        return node_values


    def calculate_hidden_layer_node_values(self,old_layer,old_node_values):
        new_node_values=[]

        for i in range(self.num_nodes_out):
            new_node_value=0

            for j in range(len(old_node_values)):
                weighted_input_derivative=old_layer.weights[i*len(old_node_values)+j]
                new_node_value+=weighted_input_derivative*old_node_values[j]
            
            new_node_value*=self.activations[i] # This time the sensitivity of the network to the inputs is calculated based on the inputs of the layer before
            new_node_values.append(new_node_value)
        
        return new_node_values


    def update_gradients(self,node_values): # Updates the gradients of the weights and biases (gradients=the slope that represents the loss, the goal is to find the number that makes it reach 0) based on the sensitivity of the inputs to the network (that is what node values does)
        for i in range(self.num_nodes_out):
            for j in range(self.num_nodes_in):
                self.cost_gradient_w[i*self.num_nodes_in+j]+=self.inputs[j]*node_values[i] 
            self.cost_gradient_b[i]=node_values[i]


    def apply_gradients(self,learn_rate,regularization,momentum): 
        weight_decay=1-regularization*learn_rate # Uses L2 regularization and momentum-velocity (later) to limit overfitting

        for i in range(len(self.weights)):
            velocity=self.weight_velocities[i]*momentum-self.cost_gradient_w[i]*learn_rate
            self.weight_velocities[i]=velocity

            self.weights[i]=self.weights[i]*weight_decay+velocity
            self.cost_gradient_w[i]=0

        for i in range(len(self.biases)):
            velocity=self.bias_velocities[i]*momentum-self.cost_gradient_b[i]*learn_rate
            self.bias_velocities[i]=velocity

            self.biases[i]+=velocity
            #print(self.biases,len(self.biases))
            self.cost_gradient_b[i]=0


class NeuralNetwork:

    def __init__(self,layer_sizes): # To initialise the weights,biases... for each layer
        self.predictions=[]
        self.layers=[]
        for i in range(len(layer_sizes)-1):
            self.layers.append(Layer(layer_sizes[i],layer_sizes[i+1]))
    

    def calculate_outputs(self,input): # Calculates the results of the neural network by using the inputs of the last layer
        for layer in self.layers:
            input=layer.calculate_outputs(input)

        self.predictions.append(input)
        return input
    

    def update_gradients(self,data_point,expected_outcome):
        self.calculate_outputs(data_point) # Adjusts the weights and biases for this datapoint
        output_layer=self.layers[len(self.layers)-1] # Last layer is the output layer

        # Calculates how sensitive the loss is to this input and updates the weights and biases accordingly, just on the output layer
        node_values=output_layer.calculate_output_layer_node_values(expected_outcome)
        output_layer.update_gradients(node_values)
    
        
        # Uses backpropagation (goes from the last hidden layer to the first, hidden layer=each layer except the first and last), to do the same as before, but this time for the hidden layer
        for i in range(len(self.layers)-2,-1,-1): 
            hidden_layer=self.layers[i]
            node_values=hidden_layer.calculate_hidden_layer_node_values(self.layers[i+1],node_values)
            hidden_layer.update_gradients(node_values)


    def learn(self,flattened_batch_training_images,flattened_batch_training_labels,learn_rate,regularization,momentum):
        for j in range(len(flattened_batch_training_images)):
            batch_data=flattened_batch_training_images[j]
            batch_expected_outcomes=flattened_batch_training_labels[j]

            # Calls the gradient descent function, for each batch, the goal is to minimise the loss (how wrong are the guesses) of the neural network
            for j in range(len(batch_data)):
                self.update_gradients(batch_data[j],batch_expected_outcomes[j])
            
            
        # Tunes the weights and biases of the network bases on the gradients found
        for layer in self.layers:
            layer.apply_gradients(learn_rate/len(batch_data),regularization,momentum) 
        
        return self.predictions
        

    def show_cost(self,inputs,expected_outputs): # Shows the cost-loss of the network (just for monitoring, it is not actually needed)
        total_cost=0
        for i in range(len(inputs)):
            outputs=self.calculate_outputs(inputs[i])
            cost=0

            for j in range(len(outputs)):
                cost+=(outputs[j]-expected_outputs[i])*(outputs[j]-expected_outputs[i]) # Show cost equation

            total_cost+=cost

        return total_cost/len(inputs)
    

    def show_accuracy(self,training_labels):
        num_correct=0
        training_labels_count=0
        for i in range(len(self.predictions)):
            if i % 20==0:
                training_labels_count=0

            #print('WHY',self.predictions[i],np.argmax(training_labels[training_labels_count]))
            if np.argmax(self.predictions[i])==np.argmax(training_labels[training_labels_count]):
                num_correct+=1
            
            training_labels_count+=1
        
        return num_correct
