
public class Board {
	private int N, M;
	private int [][] squares;
	Snake [] snakes;
	Ladder [] ladders;
	Present [] presents;
	
//Constructors
	Board(){
		N=0;
		M=0;
		squares=new int [N][M];
		snakes = new Snake[0];
		ladders= new Ladder[0];
		presents= new Present[0];
	}
	
	Board(int N, int M, int numOfSnakes, int numOfLadders, int numOfPresents) {
		this.N=N;
		this.M=M;
		squares = new int [N][M];
		snakes = new Snake[numOfSnakes];
		ladders = new Ladder[numOfLadders];
		presents = new Present[numOfPresents];
	}
	
	Board(Board b) {
		N=b.N;
		M=b.M;
		squares=new int [N][M];//commits memory
		squares=b.squares;

		snakes=new Snake[b.snakes.length];//commits memory
		for(int i=0; i<snakes.length; i++)//copy for each object separately
			snakes[i]= new Snake(b.snakes[i]);
		
		ladders=new Ladder[b.ladders.length];
		for(int i=0; i<ladders.length; i++)
			ladders[i]= new Ladder(b.ladders[i]);
		
		presents=new Present[b.presents.length];
		for(int i=0; i<presents.length; i++)
			presents[i]= new Present(b.presents[i]);
	}
	
//Setters and Getters
	public void setN(int N) {
		this.N=N;
	}
	
	public int getN() {
		return N;
	}
	
	public void setM(int M) {
		this.M=M;
	}
	
	public int getM() {
		return M;
	}
	
	public void setSquares(int[][] squares) {
		this.squares = squares;
	}
	
	public int[][] getSquares() {
		return squares;
	}
	
	public void setLadders(Ladder[] ladders) {
		this.ladders = ladders;
	}
	
	public Ladder[] getLadders() {
		return ladders;
	}
	
	public void setSnakes(Snake[] snakes) {
		this.snakes = snakes;
	}
	
	public Snake[] getSnakes() {
		return snakes;
	}
	
	public void setPresents(Present[] presents) {
		this.presents = presents;
	}
	
	public Present[] getPresents() {
		return presents;
	}

//FUNCTION THAT CREATES THE BOARD INITIALIZING SQUARES, SNAKES , LADDERS AND PRESENTS
	public void createBoard() {
		int count=1;
		int ST=0, SH=0, LD=0, LU=0, PR=0, pr_points=0, i=0;		//(int)Math.random()*(max-min)+min;
		boolean state=false;//means the ladder didn't get used
		
//places the squares from bottom to top
		for(i=N-1; i>=0; i--) {
			if((i-1)%2==0)//if i is an even number counting starts from the LEFT
				for(int j=0; j<M; j++) {
					squares[i][j]=count;
					count++;
				}
			else//if i is an odd number counting starts from the RIGHT
				for(int j=M-1; j>=0; j--) {
					squares[i][j]=count;
					count++;
				}	
		}
		
//initializes each array's values
		for(i=0; i<snakes.length; i++)
			snakes[i]=new Snake();
		for(i=0; i<ladders.length; i++)
			ladders[i]=new Ladder();
		for(i=0; i<presents.length; i++)
			presents[i]=new Present();
		
//places the snakes
		for(i=0; i<snakes.length; i++) {
			boolean same=false;
			ST=(int)(Math.random()*(N*M-M-1)+1);//tail can't be at the top line (explains -M)
	 
			do {//checks if two snakes have the same head
				same=false;
				SH=(int)(Math.random()*((N*M-1)-ST-M-1)+1+ST+M);//Head has to be on a square with bigger value
				for(int j=0; j<snakes.length; j++)					//than the tail.//+M, so as the head to be at least one line higher 
					if(SH==snakes[j].getHeadId()) {
						same=true;
						break;
					}
			}while(same);
			
			snakes[i]= new Snake(i+1, SH, ST);
		}				
		
//places the ladders
		for(i=0; i<ladders.length; i++) {
			boolean same=false, equal=false;
			do {
				equal=false;
				do {//checks if two ladders have the same bottom
					same=false;
					LD=(int)(Math.random()*(N*M-M-1)+1);//bottom can't be at the top line (explains -M)
					for(int j=0; j<ladders.length; j++)					
						if(LD==ladders[j].getBottomSquareId()) {
							same=true;
							break;
						}
				}while(same);
				
				for(int j=0; j<snakes.length; j++)//ladder's bottom and snake's head can't be on the same square
					if(LD==snakes[j].getHeadId()) { 
						equal=true;
						break;
					}
				if(!equal) {
					LU=(int)(Math.random()*((N*M-1)-LD-1-M)+1+LD+M);
					ladders[i]= new Ladder(i+1, LU, LD, state);
				}
			}while(equal);
		}
				
//places the presents
		for(i=0; i<presents.length; i++) {
			boolean same=false;
			do {//checks if two presents are on the same square
				same=false;
				PR=(int)(Math.random()*(N*M-1)+1);
				for(int j=0; j<presents.length; j++)					
					if(PR==presents[j].getPresentId()) {
						same=true;
						break;
					}
			}while(same);
				
			pr_points=(int)(Math.random()*((N*M)/4-(-(N*M)/4))-(N*M)/4);//Present's point concerned the size of the board
			presents[i]=new Present(i+1, PR, pr_points);					//between -(N*M)/4 and +
		}

	}
	
//FUNCTION THAT PRINTS THE BOARDS OF SNAKES, LADDERS AND PRESENTS SEPARATELY
	public void createElementBoard() {
		//createBoard();
		
		String [][] elementBoardSnakes= new String[N][M];
		String [][] elementBoardLadders= new String[N][M];
		String [][] elementBoardPresents= new String[N][M];

//initializing element array for snakes
		for(int i=0; i<N; i++) 
			for(int j=0; j<M; j++) 
				elementBoardSnakes[i][j]="___ ";

//initializing element array for ladders
		for(int i=0; i<N; i++) 
			for(int j=0; j<M; j++) 
				elementBoardLadders[i][j]="___ ";

//initializing element array for presents
		for(int i=0; i<N; i++) 
			for(int j=0; j<M; j++) 
				elementBoardPresents[i][j]="___ ";
		
//places properly snakes, ladders and presents on each element board correspondingly
		for(int i=0; i<N; i++) {
			for(int j=0; j<M; j++) {
				for(int k=0; k<snakes.length; k++) {
					if(squares[i][j]==snakes[k].getHeadId()) 
						elementBoardSnakes[i][j]="SH"+(k+1)+" ";
					else if(squares[i][j]==snakes[k].getTailId()) 
						elementBoardSnakes[i][j]="ST"+(k+1)+" ";
				}
				
				for(int k=0; k<ladders.length; k++) {
					if(squares[i][j]==ladders[k].getTopSquareId())
						elementBoardLadders[i][j]="LU"+(k+1)+" ";
					else if(squares[i][j]==ladders[k].getBottomSquareId())
						elementBoardLadders[i][j]="LD"+(k+1)+" ";
				}
				
				for(int k=0; k<presents.length; k++) {
					if(squares[i][j]==presents[k].getPresentSquareId())
						elementBoardPresents[i][j]="PR"+(k+1)+" ";
				}
					
			}//inside for
		}//outside for
		
//prints the element boards separately
		System.out.println("\nSNAKES");
		for(int i=0; i<N; i++) {
			for(int j=0; j<M; j++) 
				System.out.print(elementBoardSnakes[i][j]);
			System.out.println();
		}
		
		System.out.println("\n\nLADDERS");
		for(int i=0; i<N; i++) {
			for(int j=0; j<M; j++) 
				System.out.print(elementBoardLadders[i][j]);
			System.out.println();
		}
		
		System.out.println("\n\nPRESENTS");
		for(int i=0; i<N; i++) {
			for(int j=0; j<M; j++) 
				System.out.print(elementBoardPresents[i][j]);
			System.out.println();
		}
	}
}