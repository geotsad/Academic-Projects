
public class Present {
	private int presentId;
	private int presentSquareId;
	private int points;
	
//Constructors
	Present(){
		presentId=0;
		presentSquareId=0;
		points=0;
	}
	
	Present(int presentId, int presentSquareId, int points){
		this.presentId=presentId; 
		this.presentSquareId=presentSquareId;
		this.points=points;
	}
	
	Present(Present p){
		presentId=p.presentId;
		presentSquareId=p.presentSquareId;
		points=p.points;
	}
	
//Setters and Getters
	public void setPresentId(int presentId) {
		this.presentId = presentId;
	}
	
	public int getPresentId() {
		return presentId;
	}
	
	public void setPresentSquareId(int presentSquareId) {
		this.presentSquareId=presentSquareId;
	}
	
	public int getPresentSquareId() {
		return presentSquareId;
	}
	
	public void setPoints(int points) {
		this.points=points;
	}
	
	public int getPoints() {
		return points;
	}
}
