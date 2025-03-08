
public class Snake {
	private int snakeId;
	private int headId;
	private int tailId;
	
//Constructors
	Snake(){
		snakeId=0;
		headId=0;
		tailId=0;
	}
	
	Snake(int snakeId, int headId, int tailId){
		this.snakeId=snakeId; 
		this.headId=headId;
		this.tailId=tailId;
	}
	
	Snake(Snake s){
		this.snakeId=s.snakeId;
		this.headId=s.headId;
		this.tailId=s.tailId;
	}
	
//Setters and Getters
	public void setSnakeId(int snakeId) {
		this.snakeId=snakeId;
	}
	
	public int getSnakeId() {
		return snakeId;
	}
	
	public void setHeadId(int headId) {
		this.headId=headId;
	}
	
	public int getHeadId() {
		return headId;
	}
	
	public void setTailId(int tailId) {
		this.tailId = tailId;
	}
	
	public int getTailId() {
		return tailId;
	}
}