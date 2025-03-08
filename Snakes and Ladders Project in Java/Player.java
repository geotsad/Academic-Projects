
public class Player {
	private int playerId;
	private String name;
	private int score;
	Board board;
	
//Constructors
	Player(){
		playerId=0;
		name="";
		score=0;
		board = new Board();
	}
	
	Player(int playerId, String name, int score, Board board){
		this.playerId=playerId;
		this.name=name;
		this.score=score;
		this.board=new Board(board);
	}
	
//Setters and Getters
	public void setPlayerId(int playerId) {
		this.playerId = playerId;
	}
	
	public int getPlayerId() {
		return playerId;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public String getName() {
		return name;
	}
	
	public void setScore(int score) {
		this.score = score;
	}
	
	public int getScore() {
		return score;
	}
	
	public void setBoard(Board board) {
		this.board = board;
	}
	
	public Board getBoard() {
		return board;
	}
	
//Returns an array with the number of: id after his move,snakes he was bitten,ladders he used,presents he received
//Boolean pass: added because it checks if we do really make the movement or just evaluate the total points for 
//the heuristic's player POTENTIAL movement
	int[] move(int id, int die, boolean pass) {
		int[] everything = new int[4];
		int cntSnakes=0, cntLadders=0, cntPresents=0, nextId=id+die;
		boolean moreSnakes=false, moreLadders=false;
		
		
//checks if the player pass by snake's head, ladder's bottom and present
		while(moreSnakes==false || moreLadders==false) {
			moreSnakes=true;
			moreLadders=true;
			
			int i=0, j=0, k=0;
			//checks if the player's next Id is on a square that belongs on the board	
			for(i=0; i<board.getN(); i++) {
				boolean found=false;
				for(j=0;j<board.getM();j++)
					if(i<board.getN() && j<board.getM())
						if(board.getSquares()[i][j]==nextId && nextId<=board.getM()*board.getN()) {
							found=true;
							break;
						}
				if(found==true)
					break;
			}
			
			//snakes
			for(k=0; k<board.getSnakes().length; k++)
				if(i<board.getN() && j<board.getM())
					if(board.getSquares()[i][j]==board.getSnakes()[k].getHeadId() && nextId<=board.getM()*board.getN()) {
						cntSnakes+=1;
						if(pass==true)
							System.out.println("You were bitten by a snake!");
						moreSnakes=false;
						break;
					}
				
			if(moreSnakes==false)
				nextId=board.getSnakes()[k].getTailId();

				//ladders
				for(k=0; k<board.getLadders().length; k++) {
					if(i<board.getN() && j<board.getM())
						if(board.getSquares()[i][j]==board.getLadders()[k].getBottomSquareId() && nextId<=board.getM()*board.getN()) {
							if(board.getLadders()[k].getBroken()==true)//checks if a ladder is broken
								continue;                         //in order to not increase the counter
							else {
								cntLadders+=1;
								if(pass==true) {
									System.out.println("You stepped on a ladder!");
									board.getLadders()[k].setBroken(true);//each ladder can only be used once
								}
								moreLadders=false;
								break;
							}
						}	
				}
				if(moreLadders==false)
					nextId=board.getLadders()[k].getTopSquareId();

				//presents
				for(k=0; k<board.getPresents().length; k++)
					if(i<board.getN()&& j<board.getM())
						if(board.getSquares()[i][j]==board.getPresents()[k].getPresentSquareId()) {
							if(board.getPresents()[k].getPoints()==0)
								break;
							else {
								cntPresents+=1;
								score+=board.getPresents()[k].getPoints();
								if(pass==true) {
									System.out.println("You received a present!");
									board.getPresents()[k].setPoints(0);
								}
							}
						}
		}
		
		everything[0]=nextId;
		everything[1]=cntSnakes;
		everything[2]=cntLadders;
		everything[3]=cntPresents;
		
		return everything;
	}
}
