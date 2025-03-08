
public class Ladder {
	private int ladderId;
	private int topSquareId;
	private int bottomSquareId;
	private boolean broken;
	
//Constructors
	Ladder(){
		ladderId=0;
		topSquareId=0;
		bottomSquareId=0;
		broken=false;
	}
		
	Ladder(int ladderId, int topSquareId, int bottomSquareId, boolean broken){
		this.ladderId=ladderId; 
		this.topSquareId=topSquareId;
		this.bottomSquareId=bottomSquareId;
		this.broken=broken;
	}
		
	Ladder(Ladder l){//with or without THIS it's the same
		ladderId=l.ladderId;
		topSquareId=l.topSquareId;
		bottomSquareId=l.bottomSquareId;
		broken=l.broken;
	}
		
//Setters and Getters
	public void setLadderId(int ladderId) {
		this.ladderId=ladderId;
	}
		
	public int getLadderId() {
		return ladderId;
	}
		
	public void setTopSquareId(int topSquareId) {
		this.topSquareId=topSquareId;
	}
		
	public int getTopSquareId() {
		return topSquareId;
	}
		
	public void setBottomSquareId(int bottomSquareId) {
		this.bottomSquareId=bottomSquareId;
	}
		
	public int getBottomSquareId() {
		return bottomSquareId;
	}
		
	public void setBroken(boolean broken) {
		this.broken=broken;
	}
			
	public boolean getBroken() {
		return broken;
	}
}
