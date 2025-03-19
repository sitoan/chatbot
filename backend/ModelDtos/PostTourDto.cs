namespace TourFlowBE.ModelDtos{
        public class PostTourDto()
    { 
        public int? CityDestinationId { get; set; }

        public string? DepartureLocation { get; set; }

        public DateTime? StartDate { get; set; }

        public DateTime? EndDate { get; set; }

        public double? Price { get; set; }

        public int? AvailableSlots { get; set; }
        public List<string> plans { get; set; }
    } 
}