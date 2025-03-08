import java.util.*;

public class HeuristicPlayer extends Player{

	ArrayList<Integer[]> path;
	
//Constructors
	HeuristicPlayer(){
		super();
		this.path=new ArrayList<Integer[]>();
	}
	
	HeuristicPlayer(int playerId, String name, int score, Board board, ArrayList<Integer[]> path){
		super(playerId, name, score, board);
		this.path= new ArrayList<Integer[]>(path);
	}
	
//Setters and Getters
	public void setPath(ArrayList<Integer[]> path) {
		this.path = path;
	}
	
	public ArrayList<Integer[]> getPath() {
		return path;
	}
	
//Evaluates total points of player's movement without changing it's score and current position
	double evaluate(int currentPos, int dice) {
		int potentialGainPoints=0, potentialNextSquare=0, initialScore=getScore();
		int []statsOfMovement = new int[4];
		
		statsOfMovement= move(currentPos, dice, false);
		potentialNextSquare= statsOfMovement[0];
		potentialGainPoints=getScore()-initialScore;
		
		move(currentPos, 0, true);//in order the movement not to be done
		setScore(initialScore);		  //and the score to remain the same as initially
		
		return ((potentialNextSquare-currentPos)*0.7 + potentialGainPoints*0.3);
	}
	
//Function that decides which is the best movement to be executed by the Heuristic Player
	int getNextMove(int currentPos) {
		double max=0;//auxiliary variable to choose the maximum score
		int dice=0, initialScore=getScore();
		int []statsOfMovement=new int[4];
		Integer[] dicePoints=new Integer[6];
		double[] save=new double[6];
		
		//checks if the player is on the last six squares of the board in order to respect it's boundaries			   
		if(board.getM()*board.getN()-currentPos>=6)//NOT on the last six
			for(int i=0; i<6; i++)				   
				save[i]=evaluate(currentPos,i+1);
		else {
			for(int i=0; i<board.getM()*board.getN()-currentPos; i++)
				save[i]=evaluate(currentPos, i+1);
				
			for(int i=board.getM()*board.getN()-currentPos; i<6; i++)
				save[i]=evaluate(currentPos, board.getM()*board.getN()-currentPos);
		}
				
		max=save[0];
		for(int i=0; i<6; i++)
			if(save[i]>=max) {
				max=save[i];
				dice=i+1;
			}
			
			statsOfMovement=move(currentPos, dice, true);
			
			dicePoints[0]=Integer.valueOf(dice);
			dicePoints[1]=Integer.valueOf(getScore()-initialScore);
			dicePoints[2]=Integer.valueOf(statsOfMovement[0]-currentPos);
			dicePoints[3]=Integer.valueOf(statsOfMovement[1]);
			dicePoints[4]=Integer.valueOf(statsOfMovement[2]);
			dicePoints[5]=Integer.valueOf(statsOfMovement[3]);
			path.add(dicePoints);
			
			return statsOfMovement[0];
	}
	
//Prints statistics of player's movement for each round
	void statistics() {
		int numOfSnakes=0, numOfLadders=0, numOfPresents=0;
	
		for(int i=0; i<path.size(); i++)
		{
			System.out.println("ROUND "+(i+1)+":");
			System.out.println("Dice chosen-> "+path.get(i)[0]);
			System.out.println("Visits on Snake's head-> "+path.get(i)[3]);
			System.out.println("Visits on Ladder's bottom-> "+path.get(i)[4]);
			System.out.println("Visits on Present-> "+path.get(i)[5]);
			System.out.println();
			System.out.println("=============================\n");
			
			numOfSnakes+=path.get(i)[3];
			numOfLadders+=path.get(i)[4];
			numOfPresents+=path.get(i)[5];
		}
		
		System.out.println("HEURISTIC'S player TOTAL statistics: ");
		System.out.println("Total number of SNAKES conrfonted-> "+numOfSnakes);
		System.out.println("Total number of LADDERS used-> "+numOfLadders);
		System.out.println("Total number of PRESENTS received-> "+numOfPresents);
		System.out.println();
	}
}
