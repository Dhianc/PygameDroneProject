import numpy as np



class Control:
    def x_dot(self, t, x, w_):
        # Parâmetros
        w_max = 15000.  # velocidade máxima do motor
        m = 0.25  # massa
        g = 9.81  # aceleração da gravidade
        l = 0.1  # tamanho
        kf = 1.744e-08  # constante de força
        Iz = 2e-4  # momento de inércia
        tal = 0.005
        Fg = np.array([[0], [-m * g]])

        ## Estados atuais
        w = x[0:2]
        r = x[2:4]
        v = x[4:6]
        phi = x[6]
        ome = x[7]

        ## Variáveis auxiliares
        # forças
        f1 = kf * w[0] ** 2
        f2 = kf * w[1] ** 2

        # Torque
        Tc = l * (f1 - f2)

        # Força de controle
        Fc_B = np.array([[0], [(f1 + f2)]])

        # Matriz de atitude
        D_RB = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])

        ## Derivadas
        w_dot = (-w + w_) / tal
        r_dot = v
        v_dot = (1 / m) * (D_RB @ Fc_B + Fg)
        v_dot = v_dot.reshape(2, )
        phi_dot = np.array([ome])
        ome_dot = np.array([Tc / Iz])

        xkp1 = np.concatenate([w_dot,
                                r_dot,
                                v_dot,
                                phi_dot,
                                ome_dot])

        return xkp1

    def rk4(self, tk, h, xk, uk):
        k1 = self.x_dot(tk, xk, uk)
        k2 = self.x_dot(tk + h / 2.0, xk + h * k1 / 2.0, uk)
        k3 = self.x_dot(tk + h / 2.0, xk + h * k2 / 2.0, uk)
        k4 = self.x_dot(tk + h, xk + h * k3, uk)
        self.xkp1 = xk + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        return self.xkp1

    def __init__(self):
        # PARÂMETROS DE SIMULAÇÃO
        self.finished = False
        self.h = 0.005  # passo da simulação de tempo continuo
        self.Ts = 0.05  # intervalo de atuação do controlador
        self.fTh = self.Ts/self.h
        self.maxT = 600
        self.tc = np.arange(0, self.maxT, self.h)  # k
        self.td = np.arange(0, self.maxT, self.Ts)  # j
        tam = len(self.tc)
        # j = 0

        # Vetor de estados
        self.x = np.zeros([8, tam])
        self.k = 0
        # x[:, 0] = np.array([0., 0.,
        #                    0., 0.,
        #                    0., .0,
        #                    0*np.pi/180.,
        #                    0*np.pi/180.])

        # Parâmetros do sistema de controle
        self.u = np.zeros([2, len(self.td)])  # comando de controle
        self.j = 0
        # eP_ = np.zeros([2, len(td)])
        # ePm1 = 0  # erro posição k-1 (passo anterior)
        # eVm1 = 0  # erro atitude k-1 (passo anterior)

        # Constanstes do modelo
        self.m = 0.25 # massa
        self.g = 9.81  # aceleração da gravidade
        self.l = 0.1  # tamanho
        self.kf = 1.744e-08  # constante de força
        self.Iz = 2e-4  # momento de inércia
        self.tal = 0.05
        self.Fe = np.array([-self.m * self.g]) ###################################################################

        # Restrições do controle
        self.phi_max = 15 * np.pi / 180.  # ângulo máximo

        self.w_max = 15000
        self.Fc_max = self.kf * self.w_max**2  # Força de controle máximo
        self.Tc_max = self.l * self.kf * self.w_max**2

        # Waypoints
        #print("antes das posições")
        self.r_ = np.array([[0., 10.],
                            [15., 10.],
                            [-50., 2.],
                            [-20., 15.],
                            [0., 0.]]).transpose()

        
        #print("depois das posições")

        self.r_ID = 0
        self.r_IDN = 4

        # Processamento de variáveis intermediárias

        # obtem a força aplicada por cada rotor
        # f = np.zeros([3, tam])
        #
        # for k in range(tam):
        #     w = self.x[0:2, k]
        #     f[0:2, k] = np.array([self.kf * w[0] ** 2, self.kf * w[1] ** 2])
        #     f[2, k] = f[0, k] + f[1, k]  # Força total em B


    def movimenta(self, esquerda, direita, cima, baixo, comandar):
    # for k in range(tam-1):
        # Sistema de controle

        if(self.k % self.fTh) == 0:
            # Extrai os dados do  vetor
            r_k = self.x[2:4, self.k]
            v_k = self.x[4:6, self.k]
            phi_k = self.x[6, self.k]
            ome_k = self.x[7, self.k]

            # Comando de posição
            v_ = np.array([0, 0])

            # Controle de Posição
            kpP = np.array([0.075])
            kdP = np.array([0.25])
            
            if comandar == False:
                global eP
                global aP
                aP = self.r_[:, self.r_ID]
                eP = aP - r_k
                if np.linalg.norm(eP) < .1 and self.r_ID < self.r_IDN:
                    self.r_ID += 1
                if self.r_ID == self.r_IDN:
                    aP = self.r_[:, self.r_ID]
            if comandar == True:                
                if esquerda == True:
                    aP = aP + [-0.5,0]
                    if aP[0] < -54:
                        aP[0] = -54
                    print(aP)
                if direita == True:
                    aP = aP + [0.5,0]
                    if aP[0] > 20:
                        aP[0] = 20
                if cima == True:
                    aP = aP + [0,0.5]
                    if aP[1] > 16:
                        aP[1] = 16
                if baixo == True:
                    aP = aP + [0,-0.5]
                    if aP[1] < 0:
                        aP[1] = 0
            eP = aP - r_k
            print(r_k.round())


            eV = v_ - v_k
            # eP_[:, j] = eP

            # Definição do próximo waypoint


            Fx = kpP * eP[0] + kdP * eV[0]
            Fy = kpP * eP[1] + kdP * eV[1] - self.Fe #############################################################
            Fy = np.maximum(0.2 * self.Fc_max, np.minimum(Fy, 0.8 * self.Fc_max))

            # Controle de Atitude
            phi_ = np.arctan2(-Fx, Fy)

            if np.abs(phi_) > self.phi_max:
                # print(phi_*180/np.pi)
                signal = phi_ / np.absolute(phi_)
                phi_ = signal * self.phi_max

                # Limitando o ângulo
                Fx = Fy * np.tan(phi_)

            Fxy = np.array([Fx, Fy])
            Fc = np.linalg.norm(Fxy)
            f12 = np.array([Fc / 2.0, Fc / 2.0])

            # Constantes Kp e Kd
            kpA = np.array([0.75])
            kdA = np.array([0.05])
            ePhi = phi_ - phi_k
            eOme = 0 - ome_k

            Tc = kpA * ePhi + kdA * eOme
            Tc = np.maximum(-0.4 * self.Tc_max, np.minimum(Tc, 0.4 * self.Tc_max))

            # Delta de forças
            df12 = np.absolute(Tc) / 2.0

            if (Tc >= 0.0):
                f12[0] = f12[0] + df12
                f12[1] = f12[1] - df12
            else:
                f12[0] = f12[0] - df12
                f12[1] = f12[1] + df12

            # Limitadores
            w1_ = np.sqrt(f12[0] / (self.kf))
            w2_ = np.sqrt(f12[1] / (self.kf))

            # Limitando o comando do motor entre 0 - 15000 rpm
            w1 = np.maximum(0., np.minimum(w1_, self.w_max))
            w2 = np.maximum(0., np.minimum(w2_, self.w_max))

            # Determinação do comando de entrada
            self.u[:, self.j] = np.array([w1, w2])

            self.j = self.j+1

        # Simulação um passo a frente
        self.x[:, self.k + 1] = self.rk4(self.tc[self.k], self.h, self.x[:, self.k], self.u[:, self.j - 1])
        self.k += 1
        if self.k == len(self.tc) - 1:
            self.finished = True

        pos = self.x[2:4, self.k]
        angle = self.x[6, self.k]
        return pos, angle

    def is_over(self):        
        return self.finished
        print("final de control")