from rest_framework.throttling import UserRateThrottle


class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'


class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'