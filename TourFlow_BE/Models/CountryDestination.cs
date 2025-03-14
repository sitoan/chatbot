using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class CountryDestination
{
    public int Id { get; set; }

    public string? Country { get; set; }

    public virtual ICollection<CityDestination> CityDestinations { get; set; } = new List<CityDestination>();
}
