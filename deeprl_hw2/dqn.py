"""Main DQN agent."""

from keras.models import model_from_config, Sequential, Model, model_from_config
import keras.optimizers as optimizers
import keras.backend as K


class DQNAgent:
    
    GAMMA = 0.99
    ALPHA = 1e-4
    EPSILON = 0.05
    REPLAY_BUFFER_SIZE = 1000000
    BATCH_SIZE = 32
    IMG_ROWS , IMG_COLS = 84, 84
    WINDOW = 4
    TARGET_QNET_RESET_INTERVAL = 10000

    SAMPLES_BURN_IN = 10000
    TRAINING_FREQUENCY=4

    """Class implementing DQN.

    This is a basic outline of the functions/parameters you will need
    in order to implement the DQNAgnet. This is just to get you
    started. You may need to tweak the parameters, add new ones, etc.

    Feel free to change the functions and funciton parameters that the
    class provides.

    We have provided docstrings to go along with our suggested API.

    Parameters
    ----------
    q_network: keras.models.Model
      Your Q-network model.
    preprocessor: deeprl_hw2.core.Preprocessor
      The preprocessor class. See the associated classes for more
      details.
    memory: deeprl_hw2.core.Memory
      Your replay memory.
    gamma: float
      Discount factor.
    target_update_freq: float
      Frequency to update the target network. You can either provide a
      number representing a soft target update (see utils.py) or a
      hard target update (see utils.py and Atari paper.)
    num_burn_in: int
      Before you begin updating the Q-network your replay memory has
      to be filled up with some number of samples. This number says
      how many.
    train_freq: int
      How often you actually update your Q-Network. Sometimes
      stability is improved if you collect a couple samples for your
      replay memory, for every Q-network update that you run.
    batch_size: int
      How many samples in each minibatch.
    """
    def __init__(self,
                 qnetwork,
                 preprocessor,
                 memory,
                 policy=None,
                 gamma=GAMMA,
                 target_update_freq=TARGET_QNET_RESET_INTERVAL,
                 num_burn_in=SAMPLES_BURN_IN,
                 train_freq=TRAINING_FREQUENCY,
                 batch_size=BATCH_SIZE):

      
        
        #Parameters
        
        # Soft vs hard target model updates.
        if target_update_freq < 0:
            raise ValueError('`target_update_freq` must be >= 0.')
        elif target_update_freq >= 1:
            # Hard update every `target_model_update` steps.
            target_update_freq = int(target_update_freq)
        else:
            # Soft update with `(1 - target_model_update) * old + target_model_update * new`.
            target_update_freq = float(target_model_update)
        
        if num_burn_in < 0:
            raise ValueError('num_burn_in must be >=0')
        else
            self.num_burn_in=num_burn_in

        if train_freq < 0:
            raise ValueError('train_freq must be >=0')
        else
            self.train_freq=train_freq

        if batch_size < 0:
            raise ValueError('batch size must be >=0')
        else
            self.batch_size=batch_size
        pass
        
        if gamma <= 0 || gamma >1.0 :
            raise ValueError('gamma must be in [0,1]')
        else
            self.gamma=gamma



        #Internal States
        self.compiled=False
        self.training=False
        self.testing=False
        self.observing=False
            
            

        #Related Objects
        self.preprocessor=preprocessor
        self.memory=memory
        self.qnetwork=qnetwork
    
        #Agent's Policies
        
        #TODO: change policy so that alwayes each class has attribute num_actions
        if policy is None:
            self.policy = EpsGreedyQPolicy(EPSILON)
        observing_policy = UniformRandomPolicy(self.policy.num_actions)
        
        #TODO: put the arguments correctly here
        training_policy = LinearDecayGreedyEpsilonPolicy()

    @property
    def preprocessor(self):
        return self.__preprocessor
    
    @preprocessor.setter
    def policy(self, preprocessor):
        self.__preprocessor = preprocessor
    
    @property
    def memory(self):
        return self.__memory
    
    @memory.setter
    def policy(self, memory):
        self.__memory = memory
    
    @property
    def qnetwork(self):
        return self.__qnetwork
    
    @qnetwork.setter
    def qnetwork(self, qnetwork):
        self.__qnetwork = qnetwork
    

    @property
    def policy(self):
        return self.__policy
    
    @policy.setter
    def policy(self, policy):
        self.__policy = policy
    
    @property
    def target_qnetwork(self):
        return self.__target_qnetwork
    
    @target_qnetwork.setter
    def target_qnetwork(self, target_qnetwork):
            self.__target_qnetwork = target_qnetwork

    def compile(self, optimizer, loss_func):
        
        #TODO: check if this is correct
        #See line 8-16: https://github.com/matthiasplappert/keras-rl/blob/master/rl/util.py
        
        #set-up target qnetwork
        self.target_qnetwork=Sequential.from_config(self.qnetwork.get_config())
        self.target_qnetwork.set_weights(self.qnetwork.get_weights())
        
  
        
        #See 152-158: https://github.com/matthiasplappert/keras-rl/blob/master/rl/agents/dqn.py
        #TODO: Should we compile both networks??
        
        self.qnetwork.compile(loss=mean_huber_loss,optimizer=adam)
        
        self.compiled=True
        self.step=0
        

        """Setup all of the TF graph variables/ops.

        This is inspired by the compile method on the
        keras.models.Model class.

        This is a good place to create the target network, setup your
        loss function and any placeholders you might need.
        
        You should use the mean_huber_loss function as your
        loss_function. You can also experiment with MSE and other
        losses.

        The optimizer can be whatever class you want. We used the
        keras.optimizers.Optimizer class. Specifically the Adam
        optimizer.
        """
        
        pass

    def calc_q_values(self, state_batch):

        """Given a state (or batch of states) calculate the Q-values.

        Basically run your network on these states.

        Return
        ------
        Q-values for the state(s)
        """
        
        #See: https://github.com/matthiasplappert/keras-rl/blob/master/rl/agents/dqn.py
        #what does processor.process_state_batch do??
        
        q_values = self.qnetwork.predict_on_batch(state_batch)
        
        assert q_values.shape == (len(state_batch), self.policy.num_actions)

        return q_values
        
        pass

    def select_action(self, state, **kwargs):
        
        #processed_state=process_state_for_network(state)
        q_values = self.calc_q_values(state)

        if self.training
            action=self.training_policy.select_action(q_values,kwargs)
                
        if self.testing
            action=self.testing_policy.select_action(q_values,kwargs)

        if self.observing
            action=self.training_policy.select_action(kwargs)
        


        return action

        pass

    def update_policy(self):
        """Update your policy.

        Behavior may differ based on what stage of training your
        in. If you're in training mode then you should check if you
        should update your network parameters based on the current
        step and the value you set for train_freq.

        Inside, you'll want to sample a minibatch, calculate the
        target values, update your network, and then update your
        target values.

        You might want to return the loss and other metrics as an
        output. They can help you monitor how training is going.
        """
        pass

    def fit(self, env, num_iterations, max_episode_length=None):
        
        #warm-up network, fill the replay memory with some samples
        
        self.observing=True
        #TODO: see line 70, why deep copy???
        #https://github.com/matthiasplappert/keras-rl/blob/master/rl/core.py
        observation = deepcopy(env.reset())
        #process the image
        if self.preprocessor is not None:
            processed_observation = self.preprocessor.process_state_for_network(observation)
            assert processed_observation is not None
    
    
        #start filling replay memory
        for step in range(1,self.num_burn_in)
             #TODO: what is kwargs???
             #next action
             action=select_action(processed_observation,kwargs)
    
             #observe next state
             new_observation, reward, done, info = env.step(action)
             new_observation = deepcopy(new_observation)
             if self.preprocessor is not None:
                 processed_new_observation = self.preprocessor.process_state_for_network(new_observation)
                 assert processed_new_observation is not None

             if self.memory is not None:
                 self.memory.append(self,processed_observation, action, reward, new_processed_observation, is_terminal)
            
             processed_observation=new_processed_observation


        self.observing=False
        self.Training=True

        
        for episode in range(1,num_iterations)
            
            observation = deepcopy(env.reset())
            if self.preprocessor is not None:
                processed_observation = self.preprocessor.process_state_for_network(observation)
            assert processed_observation is not None
            
            for self.step in range(1,max_episode_length)
                
                action=select_action(processed_observation,kwargs)
                new_observation, reward, done, info = env.step(action)
                new_observation = deepcopy(new_observation)
                    
                if self.preprocessor is not None:
                    processed_new_observation = self.preprocessor.process_state_for_network(new_observation)
                    assert processed_new_observation is not None
                                
                if self.memory is not None:
                    self.memory.append(self,processed_observation, action, reward, new_processed_observation, is_terminal)

                self.update_policy()
                processed_observation=new_processed_observation
        

        """Fit your model to the provided environment.

        Its a good idea to print out things like loss, average reward,
        Q-values, etc to see if your agent is actually improving.

        You should probably also periodically save your network
        weights and any other useful info.

        This is where you should sample actions from your network,
        collect experience samples and add them to your replay memory,
        and update your network parameters.

        Parameters
        ----------
        env: gym.Env
          This is your Atari environment. You should wrap the
          environment using the wrap_atari_env function in the
          utils.py
        num_iterations: int
          How many samples/updates to perform.
        max_episode_length: int
          How long a single episode should last before the agent
          resets. Can help exploration.
        """

        self.training=False
        pass
    

    def evaluate(self, env, num_episodes, max_episode_length=None):
        """Test your agent with a provided environment.
        
        You shouldn't update your network parameters here. Also if you
        have any layers that vary in behavior between train/test time
        (such as dropout or batch norm), you should set them to test.

        Basically run your policy on the environment and collect stats
        like cumulative reward, average episode length, etc.

        You can also call the render function here if you want to
        visually inspect your policy.
        """
        pass

