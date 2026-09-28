from app import db
from datetime import datetime
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(20),nullable=False,default='trekker')#trekker/staff/admin
    is_approved=db.Column(db.Boolean,default=False)
    is_blacklisted=db.Column(db.Boolean,default=False)
    profile_pic=db.Column(db.String(200),nullable=True,default='default.png')
    
    #relationships-->

    #1. User->Booking(one user can make multiple bookings)
    bookings=db.relationship('Booking',back_populates='user',lazy=True)#User-->Booking(fk=user_id) so it back populates to user(relationship attribute) in the booking table 
    '''User->Booking(1:M relationship connected via fk=user_id in booking table with relationship attribute named 'user' in booking table)
    lazy is true here because it is saying run the query only when asked '''
    
    #2. User->StaffProfile(one user can have one staff profile)
    staff_profile=db.relationship('StaffProfile',back_populates='user',uselist=False)#User-->StaffProfile(fk=user_id) so it back populates to user(relationship attribute) in the StaffProfile table
    '''User->StaffProfile(1:1 relationship connected via fk=user_id in StaffProfile table with relationship attribute named 'user' in StaffProfile table), 
    uselist is False here because it should return back a single object or none because it is 1:1 relationship which implies one user has one staff profile'''

class Trek(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    difficulty=db.Column(db.String(20),nullable=False,default='Moderate')#easy,moderate,hard
    duration=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=True)
    total_slots=db.Column(db.Integer,nullable=True)
    start_date=db.Column(db.DateTime,nullable=False)
    end_date=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(20),nullable=False,default='pending')
#pending:created by admin, not yet visible/bookable by trekkers
#open:bookable by trekkers
#closed:all slots filled, not yet started
#ongoing:trek has started, not finished, not bookable
#completed:trek has ended, historical record
#cancelled:trek was removed by admin
    assigned_staff_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=True)
    description=db.Column(db.String(1000),nullable=True)
    
    #relationships->

    #3. Trek->Booking(one trek can have multiple bookings)
    bookings=db.relationship('Booking',back_populates='trek',lazy=True)#Trek-->Booking(1:M, fk=trek_id in Booking table) so it back populates to trek(relationship attribute) in the Booking table 
    '''Trek->Booking (1:M relationship connected via fk=trek_id present in Booking table with relationship 
    attribute named trek in Booking table
    '''

    #4. Trek->User(one trek can have one staff assigned to it)
    assigned_staff=db.relationship('User',foreign_keys=[assigned_staff_id],uselist=False)#Trek(fk=assigned_staff_id in trek table)->User.  
    '''Trek->User is a M:1 relationship(overall), but 1:1 from single trek perspective, which is saying one trek can have one guide/staff assigned to it(this is the reason why uselist is false).
    but also many trek can have same guide(need to check for dates clash afterwards in code).. but it is a possiblity .
    fk=assigned_staff_id is needed because user connects to trek via bookings and assigned_staff and sqlachemy would get confused
    '''

class Booking(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey("trek.id"),nullable=False)
    booking_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(20),default='booked')#booked,cancelled,completed
    payment_status=db.Column(db.String(20),default='pending')#pending,paid,failed
    user=db.relationship('User',back_populates='bookings')#Booking(fk=user_id)-->User back_populates to bookings(relationship attribute) in user table  
    trek=db.relationship('Trek',back_populates='bookings')#Booking(fk=trek_id)-->Trek back populates to bookings(relationship attribute) in trek table
    __table_args__=(db.UniqueConstraint('user_id','trek_id',name='unique_user_trek_booking'),)
    
class StaffProfile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False,unique=True)
    contact=db.Column(db.String(15),nullable=False,unique=True)
    bio=db.Column(db.String(500),nullable=True)
    rating=db.Column(db.Float,default=0.0)
    experience=db.Column(db.Float,default=0.0)
    user=db.relationship('User',back_populates='staff_profile')#StaffProfile(1:1, fk=user_id)-->User back populates to staff_profile(relationship attribute) in user table
    '''uselist=False not needed here because StaffProfile has user_id (single FK), so one profile always points to exactly one user
    uselist=False on User.staff_profile is needed because a user might have zero or one profile, and we want a single object, not a list
    '''