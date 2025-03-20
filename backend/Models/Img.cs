using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class Img
{
    public int Id { get; set; }

    public int? CityDestinationId { get; set; }

    public string? Url { get; set; }

    public virtual CityDestination? CityDestination { get; set; }
}
