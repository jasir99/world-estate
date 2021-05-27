from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=100, unique=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=50, unique=True)
    image = models.ImageField(verbose_name='image', null=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = UserManager()
    class Meta:
        db_table = "user"
        verbose_name_plural = "user"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class UserReview(models.Model):
    content = models.CharField(verbose_name='content', max_length=2000)
    rating = models.PositiveSmallIntegerField(verbose_name='rating')
    reviewingUser = models.ForeignKey(User, related_name='reviewingUser', on_delete=models.CASCADE)
    reviewedUser = models.ForeignKey(User, related_name='reviewedUser', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('reviewingUser', 'reviewedUser'))

