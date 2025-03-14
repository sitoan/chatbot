
use TourFlow_CodeFirst;

-- create trigger
Go
CREATE TRIGGER trg_DecreaseProductQuantity
ON TourOrder
AFTER INSERT
AS
BEGIN
    DECLARE @TourId INT, @Slots INT;
 
    SELECT @TourId = TourBooked, @Slots = Slots
    FROM inserted;
 
    UPDATE Tour 
    SET AvailableSlots = AvailableSlots - @Slots
    FROM Tour 
    WHERE ID = @TourId;
END;

-- insert data

insert into CountryDestination(Country)
values(N'Việt Nam')
 


INSERT INTO CityDestination (City, CountryDestinationID) VALUES
    (N'Đà Lạt', 1),       
    (N'Nha Trang', 1),       
    (N'Hà Giang', 1),       
    (N'Hà Nội', 1),       
    (N'Ninh Bình', 1),
    (N'Hạ Long', 1),
    (N'Phong Nha', 1),
    (N'Tam Đảo', 1),
    (N'Ba Vì', 1)

 
INSERT INTO Tour (CityDestinationID, DepartureLocation, StartDate, EndDate, Price, AvailableSlots) VALUES
(3, N'Sài Gòn', '2025-04-20 08:00:00', '2025-04-23 20:00:00', 11000000, 20),
(7, N'Sài Gòn', '2025-05-05 08:00:00', '2025-05-09 20:00:00', 13500000, 20),
(2, N'Sài Gòn', '2025-05-15 08:00:00', '2025-05-19 20:00:00', 12500000, 20),
(9, N'Sài Gòn', '2025-05-25 08:00:00', '2025-05-28 20:00:00', 14000000, 20),
(6, N'Sài Gòn', '2025-06-01 08:00:00', '2025-06-04 20:00:00', 11500000, 20),
(1, N'Sài Gòn', '2025-06-10 08:00:00', '2025-06-14 20:00:00', 13000000, 20),
(5, N'Sài Gòn', '2025-06-20 08:00:00', '2025-06-23 20:00:00', 12000000, 20),
(8, N'Sài Gòn', '2025-07-01 08:00:00', '2025-07-05 20:00:00', 14500000, 20),
(4, N'Sài Gòn', '2025-07-10 08:00:00', '2025-07-13 20:00:00', 11000000, 20),
(7, N'Sài Gòn', '2025-07-20 08:00:00', '2025-07-24 20:00:00', 12500000, 20);

INSERT INTO Tour (CityDestinationID, DepartureLocation, StartDate, EndDate, Price, AvailableSlots) VALUES
(3, N'Hà Nội', '2025-04-20 08:00:00', '2025-04-23 20:00:00', 11000000, 20),
(7, N'Hà Nội', '2025-05-05 08:00:00', '2025-05-09 20:00:00', 13500000, 20),
(2, N'Hà Nội', '2025-05-15 08:00:00', '2025-05-19 20:00:00', 12500000, 20),
(9, N'Hà Nội', '2025-05-25 08:00:00', '2025-05-28 20:00:00', 14000000, 20),
(6, N'Hà Nội', '2025-06-01 08:00:00', '2025-06-04 20:00:00', 11500000, 20),
(1, N'Hà Nội', '2025-06-10 08:00:00', '2025-06-14 20:00:00', 13000000, 20),
(5, N'Hà Nội', '2025-06-20 08:00:00', '2025-06-23 20:00:00', 12000000, 20),
(8, N'Hà Nội', '2025-07-01 08:00:00', '2025-07-05 20:00:00', 14500000, 20),
(4, N'Hà Nội', '2025-07-10 08:00:00', '2025-07-13 20:00:00', 11000000, 20),
(7, N'Hà Nội', '2025-07-20 08:00:00', '2025-07-24 20:00:00', 12500000, 20);


-- Tour 1: Hà Giang (4 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(1, N'Ngày 1 (20/04/2025): 08:00 khởi hành từ Sài Gòn bằng xe du lịch; 10:30 dừng chân nghỉ giải lao, thưởng thức cà phê và bánh mì; 12:30 đến Hà Giang, nhận phòng khách sạn và dùng bữa trưa với các món đặc sản vùng núi; buổi chiều, tham quan chợ địa phương và giao lưu với người dân bản địa; 19:00 dùng bữa tối và tự do khám phá khu phố cổ.'),
(1, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 khởi hành tham quan đèo Mã Pí Lèng với cảnh núi non hùng vĩ; 12:00 dừng chân dùng bữa trưa picnic ngay giữa thiên nhiên; 14:00 thăm các bản làng dân tộc, tìm hiểu phong tục tập quán và trải nghiệm văn hóa; 18:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối cùng chương trình ca nhạc dân gian.'),
(1, N'Ngày 3: 08:00 bữa sáng tại khách sạn; 09:00 tham gia tour khám phá vùng núi hoang sơ, ghé thăm các điểm check-in nổi tiếng và chụp ảnh lưu niệm; 12:00 dùng bữa trưa tại nhà hàng có tầm nhìn toàn cảnh; 14:00 tiếp tục tham quan suối nước trong xanh và thác nhỏ; 17:00 trở về khách sạn, thư giãn; 19:00 dùng bữa tối với các món đặc sản địa phương.'),
(1, N'Ngày 4 (23/04/2025): 08:00 dùng bữa sáng và trả phòng khách sạn; 09:00 tham quan nhanh chùa cổ và bảo tàng dân tộc nếu có thời gian; 11:00 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa trên đường; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 2: Phong Nha (5 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(2, N'Ngày 1 (05/05/2025): 08:00 xuất phát từ Sài Gòn bằng xe du lịch; 11:00 dừng nghỉ, thưởng thức nước ép trái cây tại trạm nghỉ; 13:00 đến Phong Nha, nhận phòng khách sạn và dùng bữa trưa với đặc sản địa phương; buổi chiều, khám phá khu vực xung quanh khách sạn và dạo chơi bên sông; 19:00 dùng bữa tối tại nhà hàng với món ăn truyền thống.'),
(2, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 bắt đầu tham quan Hang Phong Nha, khám phá thạch nhũ và hệ thống hang động kỳ vĩ; 12:00 dùng bữa trưa tại khu vực gần hang; 14:00 tham quan Hang Thiên Đường với ánh sáng lung linh tự nhiên; 17:00 trở về khách sạn, nghỉ ngơi và thưởng thức cà phê; 20:00 tự do khám phá ẩm thực đường phố.'),
(2, N'Ngày 3: 08:00 sau bữa sáng, khởi hành đi thuyền trên sông; 10:00 tham quan Hang Én, chiêm ngưỡng không gian hùng vĩ bên trong hang; 12:00 dùng bữa trưa picnic bên bờ sông; 14:00 trekking nhẹ nhàng khám phá rừng nguyên sinh xung quanh; 17:00 trở về khách sạn, thư giãn; 20:00 dùng bữa tối với thực đơn hải sản đặc trưng.'),
(2, N'Ngày 4: 08:00 bữa sáng tại khách sạn; 09:00 tham quan Làng Chài ven sông, tìm hiểu đời sống và nghề cá truyền thống; 12:00 dùng bữa trưa với cá lóc nướng và bún nước lèo; 14:00 tham quan khu bảo tồn thiên nhiên, khám phá hệ sinh thái đặc trưng của vùng; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối cùng chương trình ca nhạc dân gian.'),
(2, N'Ngày 5 (09/05/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 tham quan nhanh trung tâm Phong Nha, mua sắm đặc sản; 11:30 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa trên đường; 16:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 3: Nha Trang (5 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(3, N'Ngày 1 (15/05/2025): 08:00 khởi hành từ Sài Gòn, hành trình đến Nha Trang bắt đầu; 10:00 dừng nghỉ giải lao, thưởng thức cà phê; 12:00 đến Nha Trang, nhận phòng khách sạn và dùng bữa trưa với hải sản tươi sống; 14:00 dạo chơi bãi biển, tắm nắng và chụp ảnh; 19:00 dùng bữa tối tại nhà hàng ven biển.'),
(3, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Tháp Bà Ponagar với kiến trúc Chăm độc đáo; 12:00 dùng bữa trưa tại quán ăn địa phương; 14:00 tham quan Viện Hải dương học, tìm hiểu sinh vật biển; 17:00 tự do dạo chơi chợ đêm; 20:00 dùng bữa tối và thưởng thức cà phê đặc sản.'),
(3, N'Ngày 3: 08:00 sau bữa sáng, tham gia các hoạt động biển như lặn ngắm san hô và chèo kayak; 10:00 tham quan Hòn Mun nổi tiếng với hệ sinh thái đa dạng; 12:00 dùng bữa trưa trên du thuyền; 14:00 tham gia các trò chơi bãi biển; 17:00 trở về khách sạn, nghỉ ngơi; 20:00 dùng bữa tối với hải sản tươi sống.'),
(3, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Vinpearl Land hoặc các khu vui chơi giải trí; 12:00 dùng bữa trưa trong khu vực; 14:00 ghé thăm các điểm mua sắm và thưởng thức món ăn vặt; 17:00 tự do khám phá thành phố; 20:00 dùng bữa tối, trải nghiệm ẩm thực địa phương.'),
(3, N'Ngày 5 (19/05/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:00 tham quan nhanh chợ Nha Trang để mua sắm đặc sản; 11:00 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa; 16:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 4: Ba Vì (4 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(4, N'Ngày 1 (25/05/2025): 08:00 xuất phát từ Sài Gòn, bắt đầu hành trình đến Ba Vì; 10:30 dừng nghỉ và dùng bữa sáng nhẹ; 12:00 đến Ba Vì, nhận phòng khách sạn và dùng bữa trưa với món ăn đặc sản miền núi; 14:00 tham quan khu du lịch sinh thái với cảnh núi non và rừng xanh; 18:00 dùng bữa tối truyền thống, tự do khám phá khu vực xung quanh.'),
(4, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Vườn quốc gia Ba Vì, dạo bộ trong rừng và chiêm ngưỡng thác nước; 12:00 dùng bữa trưa picnic giữa thiên nhiên; 14:00 thăm Đền Thờ và các di tích lịch sử; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với các món đặc sản vùng núi.'),
(4, N'Ngày 3: 08:00 sau bữa sáng, tham gia trekking nhẹ quanh đồi núi, chụp ảnh phong cảnh; 10:30 thăm các điểm check-in nổi tiếng của Ba Vì; 12:00 dùng bữa trưa tại nhà hàng địa phương; 14:00 tham gia trò chơi dân gian và giao lưu với người dân địa phương; 17:00 trở về khách sạn, thư giãn; 20:00 dùng bữa tối và thưởng thức chương trình biểu diễn văn nghệ.'),
(4, N'Ngày 4 (28/05/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:00 tham quan chùa cổ hoặc khu văn hóa nếu có thời gian; 10:30 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa trên đường; 15:00 tiếp tục hành trình về Sài Gòn; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 5: Hạ Long (4 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(5, N'Ngày 1 (01/06/2025): 08:00 khởi hành từ Sài Gòn, bắt đầu chuyến đi đến Hạ Long; 11:00 đến Hạ Long, nhận phòng khách sạn và dùng bữa trưa với hải sản tươi sống tại nhà hàng ven biển; 13:00 tham quan bến du thuyền và ngắm cảnh vịnh; 16:00 đi du thuyền tham quan các đảo và hang động nổi tiếng; 19:00 dùng bữa tối trên du thuyền với đặc sản địa phương.'),
(5, N'Ngày 2: 08:00 dùng bữa sáng trên du thuyền hoặc khách sạn; 09:00 tham quan Hang Sửng Sốt và Hang Đầu Gỗ, ngắm nhìn hệ thống thạch nhũ kỳ vĩ; 12:00 dùng bữa trưa trên du thuyền; 14:00 tiếp tục tham quan các đảo nhỏ và bãi biển hoang sơ; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối tại nhà hàng ven biển.'),
(5, N'Ngày 3: 08:00 sau bữa sáng, tham gia các hoạt động ngoài trời như chèo kayak và câu mực trên boong du thuyền; 10:00 tham gia trò chơi tập thể trên du thuyền, giao lưu với các du khách; 12:00 dùng bữa trưa nhẹ trên du thuyền; 14:00 tham quan thêm các hòn đảo và chụp ảnh lưu niệm; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với thực đơn hải sản phong phú.'),
(5, N'Ngày 4 (04/06/2025): 08:00 dùng bữa sáng tại khách sạn, thu dọn hành lý và trả phòng; 09:00 tham quan nhanh chợ địa phương, mua sắm đặc sản; 10:30 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa; 15:00 tiếp tục hành trình về Sài Gòn; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 6: Đà Lạt (5 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(6, N'Ngày 1 (10/06/2025): 08:00 khởi hành từ Sài Gòn qua đường cao tốc; 10:30 dừng chân tại quán cà phê nổi tiếng, thưởng thức cà phê sữa đá; 12:00 đến Đà Lạt, nhận phòng khách sạn và dùng bữa trưa với các món đặc sản cao nguyên; 14:00 dạo chơi quanh Hồ Xuân Hương, chiêm ngưỡng kiến trúc cổ và phong cảnh se lạnh; 18:00 dùng bữa tối tại nhà hàng địa phương, khám phá ẩm thực Đà Lạt.'),
(6, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Vườn Hoa Đà Lạt với hàng trăm loài hoa đa sắc; 11:00 thăm Thung Lũng Tình Yêu, chụp ảnh lưu niệm; 12:30 dùng bữa trưa tại quán ăn địa phương; 14:00 tham quan Dinh Bảo Đại và Nhà Thờ Domain de Marie; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với các món đặc sản như lẩu gà lá é.'),
(6, N'Ngày 3: 08:00 sau bữa sáng, khởi hành tham quan Thác Datanla, trải nghiệm cáp treo và leo núi mạo hiểm; 10:30 tận hưởng không khí mát mẻ và phong cảnh thiên nhiên hoang sơ; 12:00 dùng bữa trưa picnic ngay tại khu vực thác; 14:00 tham quan Vườn Dâu, hái dâu và thưởng thức trà sữa dâu; 17:00 trở về khách sạn, thư giãn tại phòng spa; 19:00 dùng bữa tối tại khách sạn hoặc quán ăn địa phương.'),
(6, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Chợ Đà Lạt, mua sắm đặc sản và quà lưu niệm; 11:00 tham quan Làng Cù Lần hoặc các trang trại cà phê, tìm hiểu quy trình sản xuất; 12:30 dùng bữa trưa tại nhà hàng địa phương; 14:00 tham gia lớp học làm bánh mì nướng truyền thống; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối cùng gia đình du lịch.'),
(6, N'Ngày 5 (14/06/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:00 tham quan nhanh các điểm như Dinh Phương hay Hồ Tuyền Lâm; 11:00 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa trên đường; 15:00 tiếp tục hành trình về Sài Gòn; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 7: Ninh Bình (4 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(7, N'Ngày 1 (20/06/2025): 08:00 khởi hành từ Sài Gòn; 10:30 dừng nghỉ tại quán cà phê đặc trưng, thưởng thức bánh mì và cà phê; 12:00 đến Ninh Bình, nhận phòng khách sạn và dùng bữa trưa với cơm cháy Ninh Bình; 14:00 dạo bộ bên bờ sông Ngô Đồng và chụp ảnh phong cảnh; 18:00 dùng bữa tối tại quán ăn địa phương, nghỉ ngơi.'),
(7, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 bắt đầu tour tham quan Tràng An, di chuyển bằng thuyền qua các hang động tự nhiên; 12:00 dùng bữa trưa picnic bên bờ sông; 14:00 leo lên Hang Múa để ngắm toàn cảnh Ninh Bình; 17:00 trở về khách sạn, thưởng thức trà chiều; 19:00 dùng bữa tối tại quán ăn nổi tiếng.'),
(7, N'Ngày 3: 08:00 sau bữa sáng, khởi hành tham quan Cố đô Hoa Lư, tìm hiểu lịch sử các triều đại xưa; 11:00 thăm Chùa Bái Đính, chiêm ngưỡng kiến trúc ấn tượng; 12:30 dùng bữa trưa tại nhà hàng bên khu du lịch; 14:00 ghé thăm các bản làng nhỏ, giao lưu với người dân địa phương; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với ẩm thực đặc sắc.'),
(7, N'Ngày 4 (23/06/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:00 tham quan nhanh các điểm phụ như động Tam Cốc; 11:00 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa; 15:00 tiếp tục hành trình về Sài Gòn; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 8: Tam Đảo (5 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(8, N'Ngày 1 (01/07/2025): 08:00 khởi hành từ Sài Gòn qua những cung đường quanh co; 10:30 dừng nghỉ tại điểm đẹp, thưởng thức nước ép trái cây và bánh ngọt; 12:00 đến Tam Đảo, nhận phòng khách sạn và dùng bữa trưa với món ăn địa phương; 14:00 dạo quanh trung tâm, ghé thăm cửa hàng quà lưu niệm; 18:00 dùng bữa tối với lẩu Thái và gà nướng.'),
(8, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Thác Bạc, chiêm ngưỡng cảnh nước chảy xiết; 11:00 thăm đền thờ và công trình kiến trúc cổ, tìm hiểu lịch sử địa phương; 12:30 dùng bữa trưa tại quán ăn địa phương; 14:00 trekking nhẹ quanh bản làng và đồi thông; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với canh chua và cơm lam đặc trưng.'),
(8, N'Ngày 3: 08:00 sau bữa sáng, tham gia tour ngoại ô, thăm hồ Tam Đảo, thung lũng hoa và vườn dâu; 10:30 tham gia chụp ảnh tại các điểm check-in nổi tiếng; 12:00 dùng bữa trưa picnic ngoài trời; 14:00 tham quan làng nghề truyền thống, tìm hiểu quy trình sản xuất hàng thủ công; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối, tự do khám phá ẩm thực đường phố.'),
(8, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan chùa Tam Đảo và vườn hoa, tìm hiểu văn hóa tâm linh; 11:00 tham quan khu bảo tồn thiên nhiên xung quanh; 12:30 dùng bữa trưa với đặc sản vùng núi; 14:00 tham gia mua sắm quà lưu niệm và trải nghiệm làm gốm truyền thống; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối cùng chương trình ca nhạc dân gian.'),
(8, N'Ngày 5 (05/07/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:00 tham quan nhanh trung tâm Tam Đảo, ghé thăm các cửa hàng đặc sản; 10:30 khởi hành về Sài Gòn, dừng nghỉ và dùng bữa trưa trên đường; 15:00 tiếp tục hành trình về Sài Gòn; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 9: Hà Nội (4 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(9, N'Ngày 1 (10/07/2025): 08:00 khởi hành từ Sài Gòn (bằng xe du lịch hoặc chuyến bay); 10:00 đến Hà Nội, nhận phòng khách sạn và dùng bữa trưa với phở truyền thống; 12:30 dạo quanh phố cổ, ghé thăm các cửa hàng và chợ địa phương; 15:00 tham quan Hồ Hoàn Kiếm và đền Ngọc Sơn; 18:00 dùng bữa tối với bún chả và nem rán; 20:00 tản bộ quanh phố cổ, thưởng thức không khí về đêm.'),
(9, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Văn Miếu – Quốc Tử Giám, tìm hiểu lịch sử giáo dục; 11:00 thăm Lăng Chủ tịch Hồ Chí Minh và Quảng trường Ba Đình; 12:30 dùng bữa trưa tại quán ăn truyền thống; 14:00 tham quan bảo tàng Dân tộc học; 17:00 nghỉ ngơi tại quán cà phê ven hồ; 19:00 dùng bữa tối với bún đậu mắm tôm và chả cá Lã Vọng.'),
(9, N'Ngày 3: 08:00 sau bữa sáng, tham gia tour xe đạp quanh phố cổ, khám phá các ngõ nhỏ và cửa hàng truyền thống; 10:30 tham quan Công viên Thống Nhất; 12:00 dùng bữa trưa tại quán ăn gia đình; 14:00 tham gia tour ẩm thực đường phố, thưởng thức bún ốc, phở cuốn và kem tràng; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với bún thang và các món đặc sản khác.'),
(9, N'Ngày 4 (13/07/2025): 08:00 dùng bữa sáng tại khách sạn, thu dọn hành lý và trả phòng; 09:00 tham quan bảo tàng Mỹ thuật hoặc bảo tàng Lịch sử Hà Nội; 11:00 dạo chơi tại công viên, tận hưởng không khí yên bình; 12:00 dùng bữa trưa nhẹ tại quán ăn địa phương; 14:00 khởi hành về Sài Gòn, dừng nghỉ và chụp ảnh lưu niệm trên đường; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');

-----------------------------------------------------

-- Tour 10: Phong Nha (5 ngày)
INSERT INTO TourPlan (TourID, Detail) VALUES
(10, N'Ngày 1 (20/07/2025): 08:00 khởi hành từ Sài Gòn; 10:30 dừng nghỉ, thưởng thức trà và bánh ngọt tại quán cà phê địa phương; 12:00 đến Phong Nha, nhận phòng khách sạn và dùng bữa trưa với các món đặc sản Quảng Bình; 14:00 dạo chơi bên sông, chụp ảnh lưu niệm; 18:00 dùng bữa tối với món ăn truyền thống của vùng núi.'),
(10, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Hang Phong Nha cùng hướng dẫn viên, tìm hiểu quá trình hình thành hang động; 11:00 nghỉ giải lao và dùng bữa trưa gần hang; 13:00 tiếp tục tham quan Hang Thiên Đường với ánh sáng tự nhiên lung linh; 16:00 trở về khách sạn, nghỉ ngơi và thưởng thức trà chiều; 19:00 dùng bữa tối với hải sản và đặc sản địa phương.'),
(10, N'Ngày 3: 08:00 sau bữa sáng, khởi hành đi thuyền trên sông, ngắm cảnh thiên nhiên hoang sơ của Phong Nha; 11:30 tham quan Hang Én với hệ thống thạch nhũ kỳ vĩ; 12:30 dùng bữa trưa picnic bên bờ sông; 14:00 trekking nhẹ qua rừng nguyên sinh, khám phá hệ sinh thái độc đáo; 17:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối với thực đơn phong phú.'),
(10, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Làng Chài ven sông, tìm hiểu đời sống và nghề cá truyền thống; 11:00 dùng bữa trưa tại nhà hàng địa phương với cá lóc nướng và bún nước lèo; 13:00 tham gia giao lưu văn hóa cùng người dân, nghe kể chuyện dân gian và thưởng thức nhạc dân ca; 16:00 trở về khách sạn, nghỉ ngơi và chuẩn bị cho chuyến về; 19:00 dùng bữa tối và tham gia buổi lễ chia tay đoàn.'),
(10, N'Ngày 5 (24/07/2025): 08:00 dùng bữa sáng tại khách sạn, thu dọn hành lý và trả phòng; 09:00 tham quan nhanh trung tâm Phong Nha, mua sắm đặc sản và quà lưu niệm; 10:30 khởi hành về Sài Gòn, dừng nghỉ dùng bữa trưa trên đường; 15:00 tiếp tục hành trình về Sài Gòn; 18:00 về đến Sài Gòn, kết thúc chuyến đi.');



-- 2
INSERT INTO TourPlan (TourID, Detail) VALUES
(11, N'Ngày 1 (20/04/2025): 08:00 khởi hành từ Hà Nội bằng xe du lịch; 10:30 dừng nghỉ giải lao, thưởng thức cà phê và bánh mì; 12:30 đến Hà Giang, nhận phòng khách sạn và dùng bữa trưa với các món đặc sản vùng núi; buổi chiều, tham quan chợ địa phương và giao lưu với người dân bản địa; 19:00 dùng bữa tối và tự do khám phá khu phố cổ.'),
(11, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 khởi hành tham quan các cung đường đèo quanh Hà Giang; 12:00 dừng chân dùng bữa trưa picnic giữa thiên nhiên hùng vĩ; 14:00 thăm các bản làng dân tộc và tìm hiểu văn hóa địa phương; 18:00 trở về khách sạn, nghỉ ngơi; 19:00 dùng bữa tối cùng chương trình ca nhạc dân gian.'),
(11, N'Ngày 3: 08:00 bữa sáng tại khách sạn; 09:00 tham gia tour khám phá các điểm du lịch nổi bật của Hà Giang, chụp ảnh lưu niệm; 12:00 dùng bữa trưa tại nhà hàng với tầm nhìn toàn cảnh vùng núi; 14:00 tiếp tục tham quan các thắng cảnh thiên nhiên; 17:00 trở về khách sạn; 19:00 dùng bữa tối với món ăn đặc sản địa phương.'),
(11, N'Ngày 4 (23/04/2025): 08:00 dùng bữa sáng và trả phòng khách sạn; 09:00 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 18:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(12, N'Ngày 1 (05/05/2025): 08:00 khởi hành từ Hà Nội bằng xe du lịch; 11:00 dừng nghỉ trên đường, thưởng thức trà và bánh ngọt; 13:00 đến Phong Nha, nhận phòng khách sạn và dùng bữa trưa với đặc sản địa phương; buổi chiều, dạo quanh khu vực khách sạn; 19:00 dùng bữa tối và nghỉ ngơi.'),
(12, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan các hang động kỳ vĩ như Hang Phong Nha, khám phá thạch nhũ và hệ thống hang; 12:00 dùng bữa trưa picnic bên bờ sông; 14:00 tham gia trekking nhẹ trong rừng nguyên sinh; 18:00 trở về khách sạn; 20:00 dùng bữa tối với món ăn truyền thống.'),
(12, N'Ngày 3: 08:00 bữa sáng tại khách sạn; 09:00 tham gia tour thuyền khám phá Hang Thiên Đường; 12:00 dừng chân dùng bữa trưa ngoài trời; 14:00 tự do khám phá khu vực, chụp ảnh lưu niệm; 17:00 trở về khách sạn; 19:00 dùng bữa tối và thưởng thức ẩm thực địa phương.'),
(12, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan làng chài ven sông để tìm hiểu đời sống ngư dân truyền thống; 12:00 dùng bữa trưa với hải sản tươi sống; 14:00 giao lưu văn hóa cùng người dân địa phương; 17:00 trở về khách sạn; 20:00 dùng bữa tối.'),
(12, N'Ngày 5 (09/05/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 16:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(13, N'Ngày 1 (15/05/2025): 08:00 khởi hành từ Hà Nội; 10:00 dừng nghỉ giải lao, thưởng thức cà phê; 12:00 đến Nha Trang, nhận phòng khách sạn và dùng bữa trưa với hải sản tươi sống; buổi chiều, tắm biển và dạo chơi bãi biển; 19:00 dùng bữa tối và nghỉ ngơi.'),
(13, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Tháp Bà Ponagar, tìm hiểu lịch sử văn hóa Chăm; 12:00 dùng bữa trưa tại nhà hàng địa phương; 14:00 tham quan Viện Hải dương học; 17:00 tự do dạo chơi chợ đêm; 20:00 dùng bữa tối.'),
(13, N'Ngày 3: 08:00 sau bữa sáng, tham gia các hoạt động biển như lặn ngắm san hô và chèo thuyền; 11:00 thăm Hòn Mun; 12:30 dùng bữa trưa trên du thuyền; 14:00 tham gia trò chơi bãi biển; 17:00 trở về khách sạn; 19:00 dùng bữa tối với hải sản.'),
(13, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Vinpearl Land hoặc khu vui chơi giải trí; 12:00 dùng bữa trưa; 14:00 tự do mua sắm và khám phá thành phố; 17:00 trở về khách sạn; 20:00 dùng bữa tối.'),
(13, N'Ngày 5 (19/05/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 16:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(14, N'Ngày 1 (25/05/2025): 08:00 khởi hành từ Hà Nội; 09:30 dừng nghỉ trên đường, thưởng thức cà phê; 11:00 đến Ba Vì, nhận phòng khách sạn và dùng bữa trưa với món đặc sản vùng núi; buổi chiều, tham quan khu du lịch sinh thái; 18:00 dùng bữa tối và nghỉ ngơi.'),
(14, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Vườn quốc gia Ba Vì, dạo bộ trong rừng và chiêm ngưỡng thác nước; 12:00 dùng bữa trưa picnic; 14:00 tham quan các di tích lịch sử; 17:00 trở về khách sạn; 19:00 dùng bữa tối với món ăn truyền thống.'),
(14, N'Ngày 3: 08:00 sau bữa sáng, tham gia trekking quanh núi rừng, chụp ảnh phong cảnh; 11:00 ghé thăm các điểm check-in nổi bật; 12:00 dùng bữa trưa tại nhà hàng địa phương; 14:00 tham gia giao lưu văn hóa với người dân địa phương; 17:00 trở về khách sạn; 20:00 dùng bữa tối.'),
(14, N'Ngày 4 (28/05/2025): 08:00 dùng bữa sáng và trả phòng; 09:00 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 15:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(15, N'Ngày 1 (01/06/2025): 08:00 khởi hành từ Hà Nội; 10:00 dừng nghỉ, thưởng thức cà phê; 12:00 đến Hạ Long, nhận phòng khách sạn và dùng bữa trưa với hải sản tươi sống; buổi chiều, tham quan bến du thuyền và dạo chơi bên vịnh; 18:00 dùng bữa tối trên du thuyền.'),
(15, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Hang Sửng Sốt và Hang Đầu Gỗ, chiêm ngưỡng thạch nhũ kỳ vĩ; 12:00 dùng bữa trưa trên du thuyền; 14:00 tham gia hoạt động chèo kayak và câu mực; 17:00 trở về khách sạn; 19:00 dùng bữa tối.'),
(15, N'Ngày 3: 08:00 sau bữa sáng, tham gia tour tham quan các đảo nhỏ quanh Vịnh Hạ Long; 11:00 dừng nghỉ tại bãi biển hoang sơ; 12:00 dùng bữa trưa picnic; 14:00 tiếp tục khám phá hệ thống hang động; 17:00 trở về khách sạn; 19:00 dùng bữa tối với thực đơn đặc sắc.'),
(15, N'Ngày 4 (04/06/2025): 08:00 dùng bữa sáng và trả phòng; 09:00 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 15:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(16, N'Ngày 1 (10/06/2025): 08:00 khởi hành từ Hà Nội; 11:00 dừng nghỉ trên đường, thưởng thức cà phê; 13:00 đến Đà Lạt, nhận phòng khách sạn và dùng bữa trưa với ẩm thực cao nguyên; buổi chiều, dạo quanh Hồ Xuân Hương; 18:00 dùng bữa tối và nghỉ ngơi.'),
(16, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Vườn Hoa Đà Lạt, chiêm ngưỡng hàng trăm loài hoa; 12:00 dùng bữa trưa tại quán ăn địa phương; 14:00 tham quan Dinh Bảo Đại và các công trình lịch sử; 17:00 trở về khách sạn; 19:00 dùng bữa tối.'),
(16, N'Ngày 3: 08:00 sau bữa sáng, tham quan Thác Datanla, trải nghiệm cáp treo và leo núi; 11:00 thưởng thức phong cảnh thiên nhiên; 12:30 dùng bữa trưa picnic; 14:00 thăm các trang trại dâu và cà phê; 17:00 trở về khách sạn; 19:00 dùng bữa tối.'),
(16, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Chợ Đà Lạt, mua sắm đặc sản và quà lưu niệm; 12:00 dùng bữa trưa; 14:00 tham gia lớp học làm bánh mì nướng truyền thống; 17:00 trở về khách sạn; 19:00 dùng bữa tối và thư giãn.'),
(16, N'Ngày 5 (14/06/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 16:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(17, N'Ngày 1 (20/06/2025): 08:00 khởi hành từ Hà Nội; 09:30 dừng nghỉ trên đường, thưởng thức cà phê và bánh mì; 11:00 đến Ninh Bình, nhận phòng khách sạn và dùng bữa trưa với cơm cháy đặc sản; buổi chiều, dạo bộ bên sông Ngô Đồng; 18:00 dùng bữa tối và nghỉ ngơi.'),
(17, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Tràng An bằng thuyền, chiêm ngưỡng hệ thống hang động tuyệt đẹp; 12:00 dùng bữa trưa picnic bên sông; 14:00 leo lên Hang Múa để ngắm toàn cảnh Ninh Bình; 17:00 trở về khách sạn; 19:00 dùng bữa tối với đặc sản địa phương.'),
(17, N'Ngày 3: 08:00 sau bữa sáng, tham quan Cố đô Hoa Lư và chùa Bái Đính, tìm hiểu lịch sử và văn hóa; 12:30 dùng bữa trưa tại nhà hàng; 14:00 giao lưu với người dân bản địa; 17:00 trở về khách sạn; 19:00 dùng bữa tối và thưởng thức nhạc dân ca.'),
(17, N'Ngày 4 (23/06/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 15:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(18, N'Ngày 1 (01/07/2025): 08:00 khởi hành từ Hà Nội; 09:00 dừng nghỉ trên đường, thưởng thức nước ép và bánh ngọt; 11:00 đến Tam Đảo, nhận phòng khách sạn và dùng bữa trưa với đặc sản địa phương; buổi chiều, khám phá trung tâm Tam Đảo; 18:00 dùng bữa tối và nghỉ ngơi.'),
(18, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Thác Bạc và các điểm tự nhiên quanh Tam Đảo; 12:00 dùng bữa trưa tại nhà hàng địa phương; 14:00 trekking nhẹ quanh bản làng và đồi thông; 17:00 trở về khách sạn; 19:00 dùng bữa tối.'),
(18, N'Ngày 3: 08:00 sau bữa sáng, tham gia tour tham quan hồ Tam Đảo và thung lũng hoa; 11:00 chụp ảnh tại các điểm check-in nổi bật; 12:00 dùng bữa trưa picnic ngoài trời; 14:00 tham quan làng nghề truyền thống, tìm hiểu quy trình sản xuất hàng thủ công; 17:00 trở về khách sạn; 19:00 dùng bữa tối với ẩm thực địa phương.'),
(18, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan chùa Tam Đảo và vườn hoa; 11:00 khám phá khu bảo tồn thiên nhiên xung quanh; 12:00 dùng bữa trưa với đặc sản vùng núi; 14:00 mua sắm quà lưu niệm tại trung tâm Tam Đảo; 17:00 trở về khách sạn; 19:00 dùng bữa tối và nghỉ ngơi.'),
(18, N'Ngày 5 (05/07/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 15:00 về đến Hà Nội, kết thúc chuyến đi.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(19, N'Ngày 1 (10/07/2025): 08:00 khởi hành từ khách sạn tại Hà Nội; 09:00 bắt đầu hành trình khám phá các điểm du lịch nổi tiếng của Hà Nội; 11:00 tham quan Hồ Hoàn Kiếm và đền Ngọc Sơn; 12:30 dùng bữa trưa với phở truyền thống; 15:00 dạo quanh phố cổ; 18:00 dùng bữa tối và thưởng thức nghệ thuật đường phố.'),
(19, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Văn Miếu – Quốc Tử Giám và Lăng Chủ tịch Hồ Chí Minh; 12:00 dùng bữa trưa tại quán ăn địa phương; 14:00 tham quan bảo tàng Dân tộc học; 17:00 nghỉ ngơi tại quán cà phê ven hồ; 19:00 dùng bữa tối với đặc sản Hà Nội.'),
(19, N'Ngày 3: 08:00 sau bữa sáng, tham gia tour xe đạp khám phá các ngõ phố cổ; 10:00 ghé thăm Công viên Thống Nhất; 12:00 dùng bữa trưa tại quán ăn gia đình; 14:00 tham gia tour ẩm thực đường phố, thưởng thức bún ốc và nem; 17:00 trở về khách sạn; 19:00 dùng bữa tối và thưởng thức nhạc sống.'),
(19, N'Ngày 4 (13/07/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:00 tham quan bảo tàng Mỹ thuật hoặc bảo tàng Lịch sử Hà Nội; 11:00 dạo chơi công viên; 12:00 dùng bữa trưa nhẹ; 14:00 kết thúc hành trình, trở về điểm khởi hành ban đầu, kết thúc chuyến tham quan.');
INSERT INTO TourPlan (TourID, Detail) VALUES
(20, N'Ngày 1 (20/07/2025): 08:00 khởi hành từ Hà Nội; 10:30 dừng nghỉ trên đường, thưởng thức cà phê và bánh ngọt; 12:00 đến Phong Nha, nhận phòng khách sạn và dùng bữa trưa với đặc sản Quảng Bình; buổi chiều, dạo quanh khu vực khách sạn; 18:00 dùng bữa tối và nghỉ ngơi.'),
(20, N'Ngày 2: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan Hang Phong Nha cùng hướng dẫn viên, khám phá thạch nhũ và hệ thống hang; 12:00 dùng bữa trưa picnic bên sông; 14:00 tham quan Hang Thiên Đường với ánh sáng tự nhiên lung linh; 17:00 trở về khách sạn; 19:00 dùng bữa tối với hải sản địa phương.'),
(20, N'Ngày 3: 08:00 sau bữa sáng, tham gia tour thuyền khám phá hệ thống hang động; 11:00 tham quan Hang Én, chiêm ngưỡng vẻ đẹp tự nhiên; 12:30 dùng bữa trưa trên du thuyền; 14:00 trekking nhẹ qua rừng nguyên sinh, khám phá thiên nhiên hoang sơ; 17:00 trở về khách sạn; 19:00 dùng bữa tối và thư giãn.'),
(20, N'Ngày 4: 08:00 dùng bữa sáng tại khách sạn; 09:00 tham quan làng chài ven sông, tìm hiểu đời sống ngư dân và nghề cá truyền thống; 12:00 dùng bữa trưa với các món hải sản tươi sống; 14:00 giao lưu văn hóa cùng người dân địa phương; 17:00 trở về khách sạn; 19:00 dùng bữa tối và thưởng thức nhạc dân ca.'),
(20, N'Ngày 5 (24/07/2025): 08:00 dùng bữa sáng, thu dọn hành lý và trả phòng; 09:30 khởi hành về Hà Nội, dừng nghỉ dùng bữa trưa trên đường; 15:00 về đến Hà Nội, kết thúc chuyến đi.');

 

--dalat
insert into IMGs(CityDestinationID, Url) VALUES
(1,'https://unia.vn/wp-content/uploads/2023/03/dalat-city-1.jpg'),
(1,'https://dulichconvoi.com/wp-content/uploads/2019/04/da-lat-thang-12.jpg')

--nha trang
insert into IMGs(CityDestinationID, Url) VALUES
(2,'https://joyfulvietnamtravel.com/wp-content/uploads/2022/11/e5.jpg'),
(2,'https://bcp.cdnchinhphu.vn/344443456812359680/2022/12/27/nhattrang3-16721128389061596602579.jpg')

--ha giang
insert into IMGs(CityDestinationID, Url) VALUES
(3,'https://static.idctravel.com/wp-content/uploads/3/50/3-days-in-Ha-Giang-itinerary.jpg'),
(3,'https://media-cdn-v2.laodong.vn/storage/newsportal/2023/8/26/1233704/2-69.jpg')

--ha noi
insert into IMGs(CityDestinationID, Url) VALUES
(4,'https://bcp.cdnchinhphu.vn/344443456812359680/2023/2/17/hanoi-1676622709181419778501.jpg'),
(4,'https://dulichdaibang.com/theme/root/h%E1%BB%93%20ho%C3%A0n%20ki%E1%BA%BFm.jpg')

--ninhbinh
insert into IMGs  (CityDestinationID, Url) VALUES
(5,'https://media.tacdn.com/media/attractions-splice-spp-674x446/11/fb/0b/7c.jpg'),
(5,'https://img.baoninhbinh.org.vn/DATA/ARTICLES/2023/12/29/dlk-02ab6.jpg')

-- Ha Long
insert into IMGs(CityDestinationID, Url)
VALUES(6,'https://vcdn1-dulich.vnecdn.net/2022/05/07/vinhHaLongQuangNinh-1651912066-8789-1651932294.jpg?w=0&h=0&q=100&dpr=2&fit=crop&s=bAYE9-ifwt-9mB2amIjnqg'),
(6,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSh649bKBaJIvwl-6Y4kQe95DXE0rfRyOkJLw&s')

-- Phong Nha
insert into IMGs(CityDestinationID, Url) VALUES
(7,'https://imgnvsk.vnanet.vn/MediaUpload/Org/2023/08/21/vna-potal-lan-toa-y-nghia-phong-trao-hanh-dong-dep-moi-ngay-xay-dung-phong-nha-tro-thanh-diem-den-than-thien-va-an-toan-66146995-10-28-5021-11-22-29.jpg'),
(7,'https://cms.junglebosstours.com/assets/2c74649f-1ce7-49c8-a757-c98d275285e6?width=1202&height=802')

-- Tam Dao
insert into IMGs(CityDestinationID, Url) VALUES
(8,'https://mtcs.1cdn.vn/2023/05/09/cong-vien-tam-dao.jpg'),
(8,'https://eggyolk.vn/wp-content/uploads/2024/06/tam-dao-suong-mu.jpg')

-- Ba Vi
insert into IMGs(CityDestinationID, Url) VALUES
(9,'https://vcdn1-dulich.vnecdn.net/2022/06/08/du-lich-Ba-Vi-jpeg-2708-165363-4363-6062-1654674362.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=tT8fk97c37C_efHyX2eDEg'),
(9,'https://static-images.vnncdn.net/files/publish/2023/9/18/bien-may-ba-vi-1109.jpg')

