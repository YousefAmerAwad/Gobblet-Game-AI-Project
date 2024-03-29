import random
import copy

class GobbletAI:
    def __init__(self, Game, memory, difficulty_level="beginner"):
        self.Game = Game
        self.Mem = memory
        self.difficulty_level = difficulty_level
        
    def makeRobMove(self):
        if self.difficulty_level == "beginner":
            self.nLookAhead(1)
        elif self.difficulty_level == "intermediate":
            self.nLookAhead(2)
        elif self.difficulty_level == "advanced":
            self.nLookAhead(4)
        elif self.difficulty_level == "expert":
            self.nLookAhead(6)
        else:
            raise ValueError("Invalid difficulty level")
        
    def nLookAhead(self, n):
        allMoves = self.moves()
        bestSets = []
        bestRate = -99999
        for ms in allMoves:
            self.makeListMove(ms)
            lm = self.Game.lastMove
            rate = self.minimax(n, False, -99999, 99999)
            if (rate>bestRate):
                bestSets = []
                bestRate = rate
                bestSets.append(ms)
            elif (rate==bestRate):
                bestSets.append(ms)
            self.Game.undoMove(lm)
        
        if (len(bestSets)==0):
            self.makeRandMove()
            return True
        bestSet = random.choice(bestSets)
        self.makeListMove(bestSet)
        return True
            
    def minimax(self, n, isMax, alpha, beta):
        if (n==0):
            if (isMax):
                return self.evaluatePos(self.Game.currentPlayer().Color)
            return self.evaluatePos(self.Game.opposition().Color)
        allMoves = self.moves()
        if (isMax):
            bestRate = -99999
            for ms in allMoves:
                self.makeListMove(ms)
                lm = self.Game.lastMove
                rate = self.minimax(n-1, False, alpha, beta)
                bestRate = max(bestRate, rate)
                alpha = max(alpha, bestRate)
                self.Game.undoMove(lm)
                if (beta<=alpha):
                    break
            return bestRate
        else:
            bestRate = 99999
            for ms in allMoves:
                self.makeListMove(ms)
                lm = self.Game.lastMove
                rate = self.minimax(n-1, True,alpha, beta)
                bestRate = min(bestRate, rate)
                beta = min(beta, bestRate)
                self.Game.undoMove(lm)
                if (beta<=alpha):
                    break
            return bestRate
        
            
    def makeRatedMove(self):
        allMovs = self.moves()
        pc = self.Game.currentPlayer().Color
        bestrate = -99999
        bestsets = []
        for ms in allMovs:
            self.makeListMove(ms)
            lm = self.Game.lastMove
            rate = self.evaluatePos(pc)
            if (rate==bestrate):
                bestsets.append(ms)
            elif (rate>bestrate):
                bestrate = rate
                bestsets = []
                bestsets.append(ms)
            self.Game.undoMove(lm)
            
        bestset = random.choice(bestsets)
        self.makeListMove(bestset)
        return True
            
    def makeRandMove(self):
        allMovs = self.moves()
        Moveset = random.choice(allMovs)
        self.makeListMove(Moveset)
        return True

    def evaluatePos(self, color):
        Wrate = 0
        Brate = 0
        if (self.Game.checkWin('W')):
            Wrate = Wrate+99999
        if (self.Game.checkWin('B')):
            Brate = Brate+99999

        for i in range(3):
            Wrate = Wrate - self.Game.PlayerW.getTopPiece(i+1).Size*3
            Brate = Brate - self.Game.PlayerB.getTopPiece(i+1).Size*3

        for y in range(4):
            WCount = []
            BCount = []
            for x in range(4):
                p = self.Game.pieceAt(x,y)
                if (p.Color=='W'):
                    WCount.append(p)
                elif (p.Color=='B'):
                    BCount.append(p)
            for p in WCount:
                Wrate = Wrate + len(WCount)*p.Size
            for p in BCount:
                Brate = Brate + len(BCount)*p.Size

        for x in range(4):
            WCount = []
            BCount = []
            for y in range(4):
                p = self.Game.pieceAt(x,y)
                if (p.Color=='W'):
                    WCount.append(p)
                elif (p.Color=='B'):
                    BCount.append(p)
            for p in WCount:
                Wrate = Wrate + len(WCount)*p.Size
            for p in BCount:
                Brate = Brate + len(BCount)*p.Size
        

        WCount = []
        BCount = []
        for i in range(4):
            p = self.Game.pieceAt(i,i)
            if (p.Color=='W'):
                WCount.append(p)
            elif (p.Color=='B'):
                BCount.append(p)
        for p in WCount:
            Wrate = Wrate + len(WCount)*p.Size
        for p in BCount:
            Brate = Brate + len(BCount)*p.Size
        WCount = []
        BCount = []
        for i in range(4):
            p = self.Game.pieceAt(3-i,i)
            if (p.Color=='W'):
                WCount.append(p)
            elif (p.Color=='B'):
                BCount.append(p)
        for p in WCount:
            Wrate = Wrate + len(WCount)*p.Size
        for p in BCount:
            Brate = Brate + len(BCount)*p.Size
        
        if (color=='W'):
            return Wrate-Brate
        elif(color=='B'):
            return Brate-Wrate
        return 0


    def moves(self):
        InvGrab = []
        sizes = []
        dumG = copy.deepcopy(self.Game)
        BoardGrab = []
        for i in range(3):
            p = dumG.currentPlayer().getTopPiece(i+1)
            if (p.Size not in sizes):
                InvGrab.append(i+1)
                sizes.append(p.Size)
        for y in range(4):
            for x in range(4):
                if (dumG.holdBoardP(x, y)):
                    BoardGrab.append((x,y))
                    dumG = copy.deepcopy(self.Game)
        movesets = []
        for i in InvGrab:
            for y in range(4):
                for x in range(4):
                    dumG.holdInvP(i)
                    if (dumG.makeMove(x, y)):
                        movesets.append((-1,-1,x,y,i))
                    dumG = copy.deepcopy(self.Game)
                        
        for coor in BoardGrab:
            for y in range(4):
                for x in range(4):
                    dumG.holdBoardP(coor[0],coor[1])
                    if (dumG.makeMove(x, y)):
                        movesets.append((coor[0],coor[1],x,y,-1))
                    dumG = copy.deepcopy(self.Game)

        return movesets
    
    
    def holdInvP(self, i):
        self.Game.holdInvP(i)
    def holdBoardP(self, x, y):
        self.Game.holdBoardP(x, y)
    def makeMove(self, x, y):
        self.Game.makeMove(x, y)
    def makeListMove(self, moveList): 
        if (moveList[0]==-1): 
            self.holdInvP(moveList[4])
            self.makeMove(moveList[2],moveList[3])
        else: 
            self.holdBoardP(moveList[0], moveList[1])
            self.makeMove(moveList[2],moveList[3])
        
    
