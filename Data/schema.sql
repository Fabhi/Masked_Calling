drop table if exists `Twilio_Numbers`;
create table `Twilio_Numbers`(
	`Number` varchar(15) primary key);

drop table if exists `Session`;
create table `Session`(
    `SID` int primary key, 
    `Customer_No` int, 
    `Driver_No` int, 
    `Last_Update` datetime);

drop table if exists `Used_By`;
create table `Used_By`(
    `SID` int, 
    `Number` varchar(15), 
    foreign key(`SID`) references Session(`SID`), 
    foreign key(`Number`) references Twilio_Numbers(`Number`));

