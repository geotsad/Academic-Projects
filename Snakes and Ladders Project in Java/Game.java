import java.util.*;

public class Game {
	private int round;

//Constructors
	Game(){
		round=0;
	}
	
	Game(int round){
		this.round=round;
	}
	
//Setters and Getters
	public void setRound(int round) {
		this.round = round;
	}
	
	public int getRound() {
		return round;
	}

//Function that determines the order in which players play
	Map<Integer,Integer> setTurns(ArrayList<Object> players){
		Map<Integer, Integer> hm= new HashMap<Integer,Integer>();
		
		for(int i=0; i<players.size(); i++)
			hm.put(i+1, (int)(Math.random()*5+1));
		
		return hm;	
	}
	
//MAIN FUNCTION
	public static void main(String[] args) {
		int cnt=1, turn=0;//cnt is for the number of rounds
		boolean flag=false;
		
		Game g= new Game(1);
		Board b=new Board(10, 20, 3, 3, 6);
		b.createBoard();
		ArrayList<Integer[]> arrli=new ArrayList<Integer[]>();
	
//Players
		Player pR= new Player(1, "RANDOM", 0, b);
		HeuristicPlayer pH= new HeuristicPlayer(2, "HEURISTIC", 0, b, arrli);
		
		int[] savemove=new int[4];//saves information of player's MOVE function
		savemove[0]=1;
		int pHvar=1;//auxiliary variable for the type that function of the HeuristicPlayer ,int getNextMove() ,returns
		
//ArrayList
		ArrayList<Object> ar= new ArrayList<Object>();
		ar.add(pR);
		ar.add(pH);
		
//Map
		Map<Integer, Integer> hm=new HashMap<Integer, Integer>(g.setTurns(ar));
		
//The order in which players play
		if(hm.get(pR.getPlayerId())>=hm.get(pH.getPlayerId()))
			turn=1;
		else turn=2;
		
		//prints the element board
		b.createElementBoard();
		System.out.println();
		
		//the game evolves
		while(flag==false && g.getRound()<50) {
			if(turn==1) {
				savemove=pR.move(savemove[0],(int)(Math.random()*5+1), true);
				turn=2;
			}
			else if(turn==2) {
				pHvar=pH.getNextMove(pHvar);
				turn=1;
			}
			
			cnt++;
			if((cnt%2)==0)
				g.setRound(g.getRound()+1);
			
			if(savemove[0]>b.getM()*b.getN())
				flag=true;
			else if(pHvar>b.getM()*b.getN())
				flag=true;
		}
		
//Total print out
		System.out.println();
		System.out.println("Statistics of Heuristic player: ");
		System.out.println();
		pH.statistics();
		
		System.out.println("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
		System.out.println("\nTotal number of rounds played: "+(g.getRound()-1));
		
		double randomPlayer=0.7*savemove[0]+0.3*pR.getScore();
		double heuristicPlayer=0.7*pHvar+0.3*pH.getScore();
		System.out.println("Total points accumulated by the Random Player: "+randomPlayer);
		System.out.println("Total points accumulated by the Heuristic Player: "+heuristicPlayer);
			
		System.out.println();
		if(randomPlayer==heuristicPlayer)
		{
			if(savemove[0]==pHvar)
				System.out.println("DRAW!");
			else if(savemove[0]>pHvar)
				System.out.println("WINNER--> RANDOM pLayer!");
			else
				System.out.println("WINNER--> RANDOM pLayer!!");
		}
		else if(randomPlayer>heuristicPlayer)
			System.out.println("WINNER--> HEURISTIC player!");
		else
			System.out.println("WINNER--> HEURISTIC player!");	
	}
}
