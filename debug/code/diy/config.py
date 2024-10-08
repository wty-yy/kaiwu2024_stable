import numpy as np

# Hyper-parameters
class Args:
    version = "0.3_only_hitwall"  # model version
    seed = 1  # seed of the experiment
    torch_deterministic = True  # toggles pytorch's cudnn.deterministic 卷积算法是否相同
    cuda = True  # cuda

    # Algorithm specific arguments
    total_timesteps = int(1e6)  # total timesteps of the experiments
    learning_rate = 2.5e-4  # the learning rate of the optimizer 这个可以在稳定之后下降，比如除以十
    # group_lr = [2.5e-4, 2.5e-5]  # adjust learning rate by the proportion 按照步数比例调整学习率(在不启动退火的前提下)
    num_envs = 4  # the number of parallel environments
    num_steps = 128  # the number of steps to run in each environment per policy rollout 这个最好大于一个episode的长度，设置成512或者1024
    anneal_lr = False  # whether to anneal the learning rate or not 是否退火
    gamma = 0.999  # the discount factor gamma 这个要再高一些 0.999左右，也可以是1
    gae_lambda = 0.95  # the lambda for the general advantage estimation
    num_minibatches = 8  # the number of mini-batches
    update_epochs = 1  # the K epochs to update the policy
    norm_adv = False  # advantages normalization 可能不需要
    clip_coef = 0.2  # the surrogate clipping coefficient
    clip_vloss = True  # whether or not to use a clipped loss for the value function, as per the paper
    ent_coef = 1e-2  # entropy coefficient 一般设置成1e-4，在训练最优模型的时候设置成0
    # group_ent_coef = [1e-2, 1e-4]  # adjust entropy coefficient by proportion
    vf_coef = 0.5  # value function coefficient
    max_grad_norm = 0.5  # the maximum norm for the gradient clipping
    target_kl = None  # the target KL divergence threshold

    # to be filled in runtime
    batch_size = 0  # the batch size (computed in runtime) 
    minibatch_size = 0  # the mini-batch size (computed in runtime)
    num_iterations = 0  # the number of iterations (computed in runtime)

    ### Network ###
    observation_img_shape = (4, 51, 51)
    observation_vec_shape = (31,)
    obs_dim = np.prod(observation_img_shape) + observation_vec_shape[0]
    ### Environment ###
    # n_treasure = [13, 'norm', 13, 'norm']
    # n_treasure = 'norm'
    n_treasure = 8
    norm_sigma = 2.0
    ### Reward ###
    # distance
    dist_reward_coef = 1.0
    flash_dist_reward_coef = 5.0
    # repeat walk
    repeat_punish = np.array([
        [0, 0, 0, 0, 0],
        [0, 0.5, 0.8, 0.5, 0],
        [0, 0.8, 1.0, 0.8, 0],
        [0, 0.5, 0.8, 0.5, 0],
        [0, 0, 0, 0, 0],
    ], np.float32),
    # treasure
    treasure_miss_reset_episode = 100
    # repeat step
    repeat_step_thre = 0.2
    # hit wall
    walk_hit_wall_punish = 1.0
    flash_hit_wall_punish = 10.0
    # buff
    get_buff_reward = 5.0
    forget_buff_punish = 5.0

args = Args()

# Configuration
# 配置，包含维度设置，算法参数设置，文件的最后一些配置是开悟平台使用不要改动
class Config:

    # The input dimension of samples on the learner from Reverb varies depending on the algorithm used.
    # For instance, the dimension for DQN is 21624, while for target DQN, it is also 21624. Have to set
    # learner上reverb样本的输入维度, 注意不同的算法维度不一样, 比如示例代码中dqn的维度是21624, target_dqn的维度是21624
    # **注意**，此项必须正确配置，应该与definition.py中的NumpyData2SampleData函数数据对齐，否则可能报样本维度错误
    # Image: (4, 51, 51), Vector: (31,), Flash: (1,) 4*51*51+31+1+5
    SAMPLE_DIM = 10441

    # Size of observation
    # observation的维度，用户设计了自己的特征之后应该设置正确的维度
    DIM_OF_OBSERVATION = 0

    # Dimension of movement action direction
    # 移动动作方向的维度
    DIM_OF_ACTION_DIRECTION = 8

    # Dimension of flash action direction
    # 闪现动作方向的维度
    DIM_OF_TALENT = 8

    # Configuration about kaiwu usage. The following configurations can be ignored
    # 关于开悟平台使用的配置，是可以忽略的配置，不需要改动
    SUB_ACTION_MASK_SHAPE = 0
    LSTM_HIDDEN_SHAPE = 0
    LSTM_CELL_SHAPE = 0
    OBSERVATION_SHAPE = 45000
    LEGAL_ACTION_SHAPE = 2
